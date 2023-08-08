from typing import Union
from fastapi import APIRouter,Header,Request,File,UploadFile
from API.Controller.V1.tab_management import *

router = APIRouter()



@router.post("/v1/uplaodFOFile",tags=["Scangreeks FileUpload"])
def tradesFOUpload(file: UploadFile=File(...)):
    return tradesFO_upload(file)


@router.post("/v1/uplaodEQFile",tags=["Scangreeks FileUpload"])
def tradesEQUpload(file: UploadFile=File(...)):
    return tradesEQ_upload(file)

@router.get("/v1/getTab",tags=["Scangreeks Tabs"])
def getTab(authToken: Union[str, None] = Header(default=None)):
   return get_tab(authToken)


@router.get("/v1/getTabData/{id}",tags=["Scangreeks Tabs"])
def tabdata(id,authToken: Union[str, None] = Header(default=None)):
   return getTabData(id,authToken)







# @router.post("/v1/getMasterData",tags=["Scangreeks Data"])
# def get_master(request:schemas.GetMaster):
#    return getMasterData(request)









'''
date_obj = datetime.strptime(date_str, "%d%b%Y")
formatted_date = date_obj.strftime("%Y-%m-%d")
'''




