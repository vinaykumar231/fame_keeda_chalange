from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class CampaignEngagement(Base):
    __tablename__ = "campaign_engagements"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, nullable=False)
    influencer_id = Column(Integer, nullable=False)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=1)  
