from datetime import datetime
from typing import Tuple

from pydantic import BaseModel
class Image(BaseModel):
    timestamp: datetime
    dimensions: Tuple[int, int]
    filepath: str

    def __init__(self, timestamp: str, dimensions: Tuple[str, str]):
        super().__init__(timestamp=datetime.fromisoformat(timestamp), dimensions=(int(dimensions[0]), int(dimensions[1])))



m = Image(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
print(repr(m.timestamp))
#> datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))
print(m.dimensions)
#> (10, 20)
