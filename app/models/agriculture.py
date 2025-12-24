from pydantic import BaseModel
from typing import List, Optional

class Crop(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    growth_cycle_days: str # range like "90-120"
    water_needs: str  # e.g., "High", "Medium", "Low"
    description: str

class Disease(BaseModel):
    name: str
    symptoms: str
    treatment: str
    affected_crops: List[str]

class MarketPrice(BaseModel):
    crop_name: str
    price_avg_fcfa: float
    unit: str = "kg"
    trend: str # "monte", "baisse", "stable"
    last_updated: str
