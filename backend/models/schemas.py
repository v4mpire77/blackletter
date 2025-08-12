from typing import List
from pydantic import BaseModel

class ReviewResult(BaseModel):
    summary: str
    risks: List[str]
