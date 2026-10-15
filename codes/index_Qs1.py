from typing import List, Dict, Any, Tuple, Iterable, Generator, Callable
from itertools import islice
from pydantic import BaseModel, Field, ValidationError
import time
from functools import wraps
import pandas as pd
import numpy as np