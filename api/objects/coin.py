from dataclasses import dataclass
from typing import Optional


@dataclass
class Coin:
    id: str
    name: str
    symbol: str
    image: Optional[str] = None
    current_price: Optional[float] = None
    description: Optional[str] = None
