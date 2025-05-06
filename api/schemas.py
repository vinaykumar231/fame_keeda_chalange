import enum
from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class BriefRequest(BaseModel):
    brand: str
    product: str
    goal: str
    platform: str
    hashtags: list[str]
    persona: str
    angle: str

class BriefResponse(BaseModel):
    caption: str
    hookIdeas: list[str]
    hashtags: list[str]
    CTA: str
    tone: str

class HookIdeaResponse(BaseModel):
    hook_idea: str

    class Config:
        orm_mode = True

class HashtagResponse(BaseModel):
    hashtag: str

    class Config:
        orm_mode = True

class CTAResponse(BaseModel):
    cta: str

    class Config:
        orm_mode = True

class CampaignBriefResponse(BaseModel):
    id: int
    caption: str
    tone: str
    hook_ideas: List[HookIdeaResponse]
    hashtags: List[HashtagResponse]
    ctas: List[CTAResponse]

    class Config:
        orm_mode = True