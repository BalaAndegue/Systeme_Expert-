from pydantic import BaseModel
from typing import List, Optional

class Region(BaseModel):
    name: str
    capital: str
    climate_description: str
    soil_types: List[str]
    major_crops: List[str]
    description: Optional[str] = None
