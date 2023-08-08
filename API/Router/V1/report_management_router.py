import csv
from typing import Union
from fastapi import APIRouter,Header
import os
from Services import schemas
from API.Controller.V1.report_management import *

router = APIRouter()

@router.get("/v1/getTradeHistory",tags=["Scangreeks Report"])
# def trade_History(authToken: Union[str, None] = Header(default=None)):
async def trade_History(page: int = 1, page_size: int = 100, authToken: Union[str, None] = Header(default=None)):
   return await getTradeHistory(page,page_size,authToken)


@router.get("/v1/getNetPosition",tags=["Scangreeks Report"])
def get_position(page: int = 1, page_size: int = 100, authToken: Union[str, None] = Header(default=None)):
   return getNetPosition(page,page_size,authToken)


@router.get("/v1/getTradeHistoryfilter",tags=["Scangreeks Report"])
def getTradeHistory_filter(authToken: Union[str, None] = Header(default=None)):
   return getTradeHistoryfilter(authToken)


