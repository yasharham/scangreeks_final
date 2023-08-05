from typing import Union
from API.Controller.V1.user_management import *
from fastapi import APIRouter,Header,Request
from Services import schemas




router = APIRouter()


@router.post("/v1/signup", tags=['Scangreeks User'])
def userSignUp(request: schemas.User):
    return signup_user(request)


@router.post("/v1/login",tags=['Scangreeks User'])
def userLogin(request:schemas.UserLogin,req:Request):
    return login(request,req)


@router.get("/v1/user/",tags=['Scangreeks User'])
def get_user(authToken: Union[str, None] = Header(default=None)):
    return getUser(authToken)


@router.put("/v1/user_update/",tags=['Scangreeks User'])
def user_update(request: schemas.UpdateUser,authToken: Union[str, None] = Header(default=None)):
    return updateUser(request,authToken)


@router.put("/v1/admin_user_update/{id}",tags=['Scangreeks User'])
def adminupdate(id,request: schemas.UpdateUser,authToken: Union[str, None] = Header(default=None)):
    return adminUpdate(id,request,authToken)


@router.put("/v1/buyPlan/{name}",tags=['Scangreeks User'])
def buy_plan(name,request:schemas.Payment,authToken: Union[str, None] = Header(default=None)):
    return buyPlan(name,request,authToken)


@router.post("/v1/add_plan", tags=['Scangreeks Plans'])
def addPlan(request:schemas.Plan,authToken: Union[str, None] = Header(default=None)):
    return addNewPlan(request,authToken)
@router.put("/v1/update_plan/{id}", tags=['Scangreeks Plans'])
def updateP(id,request:schemas.Updateplan,authToken: Union[str, None] = Header(default=None)):
    return updatePlan(id,request,authToken)

@router.get("/v1/get_plan/{name}", tags=['Scangreeks Plans'])
def get_plan(name):
    return getPlan(name)

@router.get("/v1/delete_plan/{id}", tags=['Scangreeks Plans'])
def del_plan(id,authToken: Union[str, None] = Header(default=None)):
    return deletePlan(id,authToken)

@router.get("/v1/getallplan",tags=['Scangreeks Plans'])
def get_all_plan():
    return getallplan()


@router.post("/v1/add_Feature", tags=['Scangreeks Feature'])
def addF(request):
    return addFeature(request)


@router.put("/v1/update_Feature/{id}", tags=['Scangreeks Feature'])
def updateF(id,request):
    return updateFeature(id,request)


@router.delete("/v1/delete_Feature/{id}", tags=['Scangreeks Feature'])
def deleteF(id):
    return deleteFeature(id)


@router.get("/v1/get_all_features", tags=['Scangreeks Features'])
def getF():
    return getFeature()





