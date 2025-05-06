import csv
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from api.models.influencers import CampaignEngagement
from dotenv import load_dotenv
import os
import logging
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import redis
import time


load_dotenv()
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/load-campaign-engagements/")
def load_campaign_engagements(db: Session = Depends(get_db)):
    file_path = r"D:\Vinay\app\performance.csv"
    
    # Check if the file exists
    if not os.path.exists(file_path):
        return {"error": f"File '{file_path}' not found."}

    start_time = time.time()
    inserted = 0

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                campaign_id = int(row["campaignId"])

                
                influencer_id_str = row["influencerId"]
                influencer_id = int(influencer_id_str.split('_')[-1]) 


                likes = int(row.get("likes", 0))
                comments = int(row.get("comments", 0))
                shares = int(row.get("shares", 0))
                views = int(row.get("views", 1)) or 1  

                engagement = CampaignEngagement(
                    campaign_id=campaign_id,
                    influencer_id=influencer_id,
                    likes=likes,
                    comments=comments,
                    shares=shares,
                    views=views
                )

                db.add(engagement)
                inserted += 1

            except Exception as e:
                logger.error(f"Skipping row: {row}, Error: {e}")
                continue

    db.commit()
    duration = round(time.time() - start_time, 2)

    return {
        "message": f"{inserted} campaign engagement records loaded.",
        "time_taken_seconds": duration
    }

@router.get("/top-campaign-engagements/")
def get_top_campaign_engagements(db: Session = Depends(get_db), limit: int = 5):
    subquery = db.query(
        CampaignEngagement.campaign_id,
        CampaignEngagement.influencer_id,
        CampaignEngagement.likes,
        CampaignEngagement.comments,
        CampaignEngagement.shares,
        CampaignEngagement.views,
        func.coalesce(
            ((CampaignEngagement.likes + CampaignEngagement.comments + CampaignEngagement.shares) / CampaignEngagement.views) * 100, 0
        ).label('engagement_rate'),
        
        func.row_number().over(
            order_by=func.coalesce(
                ((CampaignEngagement.likes + CampaignEngagement.comments + CampaignEngagement.shares) / CampaignEngagement.views) * 100, 0
            ).desc()
        ).label('rank')
    ).subquery()

    top_engagements = db.query(
        subquery.c.campaign_id,
        subquery.c.influencer_id,
        subquery.c.likes,
        subquery.c.comments,
        subquery.c.shares,
        subquery.c.views,
        subquery.c.engagement_rate,
        subquery.c.rank
    ).limit(limit).all()

    return [{"campaign_id": engagement.campaign_id,
             "influencer_id": engagement.influencer_id,
             "likes": engagement.likes,
             "comments": engagement.comments,
             "shares": engagement.shares,
             "views": engagement.views,
             "engagement_rate": engagement.engagement_rate,
             "rank": engagement.rank} for engagement in top_engagements]