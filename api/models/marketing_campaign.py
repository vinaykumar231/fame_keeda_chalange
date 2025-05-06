from sqlalchemy import Column, ForeignKey, Integer, String, Text
from database import Base
from sqlalchemy.orm import relationship

class CampaignBrief(Base):
    __tablename__ = 'campaign_briefs'

    id = Column(Integer, primary_key=True, index=True)
    caption = Column(Text, nullable=False)
    tone = Column(Text, nullable=False)

    # Relationships
    hook_ideas = relationship("HookIdea", back_populates="brief")
    hashtags = relationship("Hashtag", back_populates="brief")
    ctas = relationship("CTA", back_populates="brief")


class HookIdea(Base):
    __tablename__ = 'hook_ideas'

    id = Column(Integer, primary_key=True, index=True)
    brief_id = Column(Integer, ForeignKey('campaign_briefs.id'), nullable=False)
    hook_idea = Column(Text, nullable=False)

    brief = relationship("CampaignBrief", back_populates="hook_ideas")


class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, primary_key=True, index=True)
    brief_id = Column(Integer, ForeignKey('campaign_briefs.id'), nullable=False)
    hashtag = Column(String(255), nullable=False)  # ✅ Fixed

    brief = relationship("CampaignBrief", back_populates="hashtags")


class CTA(Base):
    __tablename__ = 'ctas'

    id = Column(Integer, primary_key=True, index=True)
    brief_id = Column(Integer, ForeignKey('campaign_briefs.id'), nullable=False)
    cta = Column(Text, nullable=False)

    brief = relationship("CampaignBrief", back_populates="ctas")
