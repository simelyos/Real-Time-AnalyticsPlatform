from fastapi import FastAPI
from fastapi.responses import FileResponse

from src.analytics.repository import AnalyticsRepository
from src.analytics.service import AnalyticsService


app = FastAPI()