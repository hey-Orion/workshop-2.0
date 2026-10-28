# solved
Make a GET requests to an API with query parameters {"page": 1, "limit": 50} and an Authorization: Bearer <token> header. 
Return the parsed JSON.

import requests


Send a POST requests with a JSON body and a 10-second timeout. Raise an error on a 4xx or 5xx response, and return the response’s JSON.

import requests


Wrap a requests in try/except that handles Timeout, HTTPError and any other requests error separately, and returns None with a log message for each case.

from typing import Literal
from pydantic import BaseModel, Field
