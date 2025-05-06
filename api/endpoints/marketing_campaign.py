import json
import re
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
from fastapi import Depends, FastAPI, HTTPException, APIRouter
import psutil
from pydantic import BaseModel
import redis
from api.models.marketing_campaign import CTA, CampaignBrief, Hashtag, HookIdea
from database import get_db
from llm import generate_campaign_brief
from prompt import generate_prompt
from tools import creative_angle, persona_classifier, trend_fetcher
from ..schemas import BriefRequest,BriefResponse, CTAResponse, CampaignBriefResponse, HashtagResponse, HookIdeaResponse
from sqlalchemy.orm import Session, joinedload
from fastapi.encoders import jsonable_encoder
import json


load_dotenv()
router = APIRouter()
logger = logging.getLogger(__name__)

CACHE_KEY = "all_campaigns"
CACHE_TTL = 60  


# ---------------------- FastAPI Route ----------------------


@router.post("/generate-brief", response_model=BriefResponse)
def generate_brief(req: BriefRequest, db: Session = Depends(get_db)):
    try:
        trends = trend_fetcher(req.brand, req.platform)
        persona = persona_classifier(req.goal, req.product)
        angles = creative_angle(req.brand, req.product, req.goal)
        prompt = generate_prompt(req.brand, req.product, req.goal, req.platform, trends, persona, angles)

        # --- Call LLM ---
        raw = generate_campaign_brief(prompt)
        if not raw:
            raise HTTPException(500, "LLM response is empty")

        cleaned = raw.strip()

        if "```json" in cleaned:
            cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```", 2)[1].strip()

        cleaned = cleaned.replace("\n", " ").replace("    ", " ")
        cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)

        if not cleaned:
            raise HTTPException(500, "LLM response is empty after cleaning")

        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise HTTPException(500, f"Error parsing LLM response as JSON: {e}")

        elements = payload.get("campaign_brief", {}).get("campaign_elements", {})

        # --- Create Campaign Brief and Related Entries ---
        campaign_brief = CampaignBrief(
            caption=elements.get("caption", ""),
            tone=elements.get("tone_of_voice", ""),
        )

        db.add(campaign_brief)
        db.commit()
        db.refresh(campaign_brief)  # 

        # --- Hook Ideas ---
        for hook_idea in elements.get("creative_hooks", []):
            hook_idea_entry = HookIdea(
                brief_id=campaign_brief.id,
                hook_idea=hook_idea
            )
            db.add(hook_idea_entry)

        # --- Hashtags ---
        for hashtag in elements.get("hashtags", []):
            hashtag_entry = Hashtag(
                brief_id=campaign_brief.id,
                hashtag=hashtag
            )
            db.add(hashtag_entry)

        # --- CTA ---
        cta = elements.get("call_to_action", "")
        if cta:
            cta_entry = CTA(
                brief_id=campaign_brief.id,
                cta=cta
            )
            db.add(cta_entry)

        # Commit the transaction to save everything at once
        db.commit()

        # Return the response with saved data
        return BriefResponse(
            caption=elements.get("caption", ""),
            hookIdeas=elements.get("creative_hooks", []),
            hashtags=elements.get("hashtags", []),
            CTA=elements.get("call_to_action", ""),
            tone=elements.get("tone_of_voice", "")
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()  # Ensure rollback on error
        raise HTTPException(500, f"Internal server error: {e}")



redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)




    
@router.get("/campaigns", response_model=List[CampaignBriefResponse])
def get_campaigns(db: Session = Depends(get_db)):
    try:
        cached_campaigns = redis_client.get(CACHE_KEY)

        if cached_campaigns:
            logger.debug("data_fetch: Cache hit - Returning data from Redis.")
            return json.loads(cached_campaigns) 

        logger.debug("data_fetch: Cache miss - Fetching data from database.")
        
        campaigns = db.query(CampaignBrief).all()

        campaign_data = []
        for campaign in campaigns:
            logger.debug(f"data_fetch: Fetching related data for campaign ID {campaign.id}...")

            hashtags = db.query(Hashtag).filter(Hashtag.brief_id == campaign.id).all()
            hashtags_list = [HashtagResponse(hashtag=h.hashtag) for h in hashtags]

            hook_ideas = db.query(HookIdea).filter(HookIdea.brief_id == campaign.id).all()
            hook_ideas_list = [HookIdeaResponse(hook_idea=h.hook_idea) for h in hook_ideas]

            ctas = db.query(CTA).filter(CTA.brief_id == campaign.id).all()
            ctas_list = [CTAResponse(cta=c.cta) for c in ctas]

            campaign_data.append(CampaignBriefResponse(
                id=campaign.id,
                caption=campaign.caption,
                tone=campaign.tone,
                hashtags=hashtags_list,
                hook_ideas=hook_ideas_list,
                ctas=ctas_list
            ))

        logger.debug("data_fetch: Caching the campaign data in Redis.")
        
        redis_client.set(CACHE_KEY, json.dumps(jsonable_encoder(campaign_data)), ex=CACHE_TTL)

        logger.debug("data_fetch: Campaign data successfully cached in Redis.")

        return campaign_data  

    except Exception as e:
        logger.error(f"Error fetching campaigns: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching campaigns: {str(e)}")