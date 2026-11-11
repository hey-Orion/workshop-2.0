def parse_log_line(line):
    parts = line.split(" | ")
    if len(parts) != 3:
        return None
    return {
        "timestamp": parts[0],
        "level": parts[1],
        "message": parts[2]
    }


max_temps = df.groupby('sensor_id')['temp'].max().reset_index()
result = max_temps[max_temps['temp'] > 100.00]


from typing import Literal
from pydatic import BaseModel

class SR(BaseModel):
    sensor_id: int
    reading: float 
    status: Literal['a', 'i']

