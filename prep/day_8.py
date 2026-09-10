import os
import pytest
import requests
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Float, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

