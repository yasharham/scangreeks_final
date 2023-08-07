import traceback
import getmac
from datetime import date
from Services.db import mydb
from Settings.api_responses import *
from fastapi.security import OAuth2PasswordBearer
from Middleware.authenticate import *


auth_handle = AuthHandler()


'''-------------------------------------------User Management------------------------------------------------'''

def signup_user(request):
    try:
        cursor = mydb.cursor()

        # Check if field already exists in the user table
        find_user = '''SELECT Client_id FROM User WHERE Client_id = %s'''
        find_email = '''SELECT Email FROM User WHERE Email = %s'''
        find_mobile_no  = '''SELECT Mobile_no FROM User WHERE Mobile_no = %s'''

        cursor.execute(find_user,(request.Client_id,))
        user_exist = cursor.fetchone()
        print(user_exist)
        if not user_exist:
            # checks email format
            if email(request.Email):
                # checks if user exist
                cursor.execute(find_email,(request.Email,))
                email_exist = cursor.fetchone()
                if not email_exist:
                    # checks if mobile_no exist
                    cursor.execute(find_mobile_no,(request.Mobile_no,))
                    mobile_exist = cursor.fetchone()
                    if not mobile_exist:
                        # checks password length
                        if len(request.Password) >= 8:
                            password = auth_handle.get_pwd_hash(request.Password)
                            addUser = '''INSERT INTO User (Client_id, Email, Mobile_No, Password) 
                                                              VALUES (%s, %s, %s, %s)'''
                            cursor.execute(addUser,(request.Client_id, request.Email, request.Mobile_no, password))
                            mydb.commit()
                            cursor.close()
                            return signUpResponse[200]
                        else:
                            signUpResponse[406]['message'] = 'password length must be 8 or more'
                            return signUpResponse[406]
                    else:
                        signUpResponse[413]['message'] = 'mobile already in use'
                        return signUpResponse[413]
                else:
                    signUpResponse[413]['message'] = 'email already in use'
                    return signUpResponse[413]
            else:
                signUpResponse[406]['message'] = 'Invalid Email Format'
                return signUpResponse[406]
        else:
            return signUpResponse[400]
    except:
        print(traceback.print_exc())
        return response[500]


def login(request,req):
    # query1 = '''UPDATE User SET IP_Address = %s,MAC_address = %s WHERE Client_id = %s '''
    # IP_address = req.client.host
    # mac_address = getmac.get_mac_address(ip=IP_address)
    try:
        cursor = mydb.cursor()
        find_user = '''SELECT Client_id,Password FROM User WHERE Client_id = %s'''
        cursor.execute(find_user, (request.Client_id,))
        user_exist = cursor.fetchone()
        cursor.close()
        if user_exist:
            if auth_handle.verify_pwd(plain_pwd=request.Password, hashed_pwd=user_exist[1]):
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": user_exist[0]}, expires_delta=access_token_expires
                )

                loginResponses[200]['token'] = access_token
                return loginResponses[200]
            else:
                return loginResponses[401]
        else:
            return loginResponses[401]
    except:
        print(traceback.print_exc())
        return response[500]


def get_user(token):
    data = decode_access_token(token)
    cursor = mydb.cursor()
    cursor.execute('''select Client_id,Email from User where Client_id = %s  ''',(data.username,))
    user = cursor.fetchone()
    print(user)
    cursor.close()
    return {"Client":user[0],"Email":user[1]}








# def buyPlan(name, request, token):
#     data = decode_access_token(token)
#     if data.role == "user":
#         if data and name:
#             user = user_collection.find_one({"username": data.username}, {"_id": 0})
#             if user['active_plan'] == "":
#                 selected_plan = plan_collection.find_one({"plan_name": name.title()}, {"plan_name": 1, "_id": 0})
#                 user_collection.update_one({"username": data.username},
#                                            {'$set': {'active_plan': selected_plan["plan_name"]}})
#                 begindate = date.today()
#                 validity = date.today() + timedelta(days=30 * int(request.validity))
#                 payment_statement_collection.insert_one(
#                     {"username": data.username, "plan_name": name, "amount": request.amount, "validity": str(validity),
#                      "purchase": str(begindate), 'status': "Active"})
#                 return {"detail": "plan Added"}
#             else:
#                 return {"detail": "Already Exist"}
#     else:
#         return {"detail": "Not Authorized"}
#
#
# def updateUser(request, token):
#     data = decode_access_token(token)
#     user = {}
#     if request.name:
#         user.update({"name": request.name})
#
#     if request.email:
#         if email(request.email):
#             exist_email = list(user_collection.find({'email': request.email}, {'email': 1, '_id': 0}))
#             if not exist_email:
#                 user.update({"email": request.email})
#             else:
#                 raise HTTPException(status_code=400, detail="Email already registered")
#         else:
#             raise HTTPException(status_code=400, detail="Email should be in 'xyz@xyz.com' format")
#
#     if request.phone_number:
#         if len(str(request.phone_number)) == 10:
#             exist_phone = list(
#                 user_collection.find({'phone_number': request.phone_number}, {'phone_number': 1, '_id': 0}))
#             if not exist_phone:
#                 user.update({"phone_number": request.phone_number})
#             else:
#                 raise HTTPException(status_code=400, detail="Phone Number already exist")
#         else:
#             raise HTTPException(status_code=400, detail="Phone Number Valid")
#
#     user_collection.update_one({'username': data.username}, {'$set': user})
#     return {'detail': "Updated"}
#
#
# def adminUpdate(id, request, token):
#     data = decode_access_token(token)
#     if data.role == 'admin':
#         objInstance = ObjectId(id)
#         user = {}
#         if request.name:
#             user.update({"name": request.name})
#
#         if request.email:
#             if email(request.email):
#                 exist_email = list(user_collection.find({'email': request.email}, {'email': 1, '_id': 0}))
#                 if not exist_email:
#                     user.update({"email": request.email})
#                 else:
#                     raise HTTPException(status_code=400, detail="Email already registered")
#             else:
#                 raise HTTPException(status_code=400, detail="Email should be in 'xyz@xyz.com' format")
#
#         if request.phone_number:
#             if len(str(request.phone_number)) == 10:
#                 exist_phone = list(
#                     user_collection.find({'phone_number': request.phone_number}, {'phone_number': 1, '_id': 0}))
#                 if not exist_phone:
#                     user.update({"phone_number": request.phone_number})
#                 else:
#                     raise HTTPException(status_code=400, detail="Phone Number already exist")
#             else:
#                 raise HTTPException(status_code=400, detail="Phone Number Valid")
#
#         user_collection.update_one({'_id': objInstance}, {'$set': user})
#         return {'detail': "Updated"}
#     else:
#         return {"Error": "Not Authorized"}
#
#
# '''-------------------------------------------PLan Management------------------------------------------------'''
#
#
# def addNewPlan(request, token):
#     data = decode_access_token(token)
#     if data.role == "admin":
#         if not plan_collection.find_one({"plan_name": request.plan_name}):
#             plan = {"plan_name": request.plan_name, "price": request.price}
#             features = list(feature_collection.find({}, {"name": 1, "_id": 0}))
#             for i in features:
#                 if i["name"] in request.features:
#                     plan.update({i['name']: True})
#                 else:
#                     plan.update({i['name']: False})
#             plan_collection.insert_one(plan)
#             return {"detail": 'added'}
#         else:
#             return {"detail": 'Alrady exist'}
#     else:
#         return {"error": 'not authorized'}
#
#
# def updatePlan(id, request, token):
#     print(request)
#     data = decode_access_token(token)
#     if data.role == "admin":
#         if request.features:
#             features = list(feature_collection.find({}, {"name": 1, "_id": 0}))
#             for i in features:
#                 if i["name"] in request.features:
#                     plan_collection.update_one({"plan_name": id.title()}, {'$set': {i['name']: True}})
#                 else:
#                     plan_collection.update_one({"plan_name": id.title()}, {'$set': {i['name']: False}})
#         # if request.plan_name:
#         #     plan_collection.update_one({"plan_name":id.title()},{'$set':{"plan_name": request.plan_name}})
#         if request.price:
#             plan_collection.update_one({"plan_name": id.title()}, {'$set': {"price": request.price}})
#         return {"detail": "Updated"}
#     else:
#         return {"error": "Not Auhorized"}
#
#
# def getPlan(name):
#     plan = plan_collection.find_one({"plan_name": name.title()}, {"_id": 0})
#     if plan:
#         data = plan.copy()
#         for i in plan.items():
#             if not i[1]:
#                 del data[i[0]]
#         return data
#     else:
#         return {'error': "No Plan Exist"}
#
#
# def deletePlan(id, authToken):
#     data = decode_access_token(authToken)
#     if data.role == "admin":
#         if plan_collection.find_one({"_id": ObjectId(id)}):
#             plan_collection.delete_one({"_id": ObjectId(id)})
#             return {"msg": "Successfully Deleted"}
#         else:
#             return {"msg": "No Plan Exist"}
#     else:
#         return {"msg": "Not authorized"}
#
#
# def getallplan():
#     plans = list(plan_collection.find({}, {'_id': 0}))
#     return {"data": plans}
#
#
# '''-------------------------------------------Feature Management------------------------------------------------'''
#
#
# def addFeature(request):
#     if not feature_collection.find_one({"name": request}, {"name": 1, "_id": 0}):
#         feature_collection.insert_one({'name': request})
#         plan_collection.update_many({}, {'$set': {request: False}}, upsert=False, array_filters=None)
#         return {"detail": 'Feature Added'}
#     else:
#         return {"detail": 'Already Exist'}
#
#
# def updateFeature(id, request):
#     objInstance = ObjectId(id)
#     feature = feature_collection.find_one({"_id": objInstance}, {"name": 1, "_id": 0})
#     if feature_collection.find_one({"_id": objInstance}):
#         feature_collection.update_one({'_id': objInstance}, {'$set': {"name": request}})
#         plan_collection.update_many({}, {'$rename': {feature["name"]: request}}, upsert=False, array_filters=None)
#         return {"detail": 'Feature Updated'}
#     else:
#         return {"detail": 'Feature not Exist'}
#
#
# def deleteFeature(id):
#     objInstance = ObjectId(id)
#     feature = feature_collection.find_one({"_id": objInstance}, {"name": 1, "_id": 0})
#     if feature_collection.find_one({"_id": objInstance}):
#         feature_collection.delete_one({'_id': objInstance})
#         plan_collection.update_many({}, {'$unset': {feature["name"]: ""}}, upsert=False, array_filters=None)
#         return {"detail": 'Feature Deleted'}
#     else:
#         return {"detail": 'Feature not Exist'}
#
#
# def getFeature():
#     feature_list = list(feature_collection.find({}, {'_id': 0}))
#     return {'features': feature_list}
#
#
# '''
# # Fetch api
# feature_collection = requests.get(f'http://127.0.0.1:8000/v1/getfeaure/{request.plan_name}')
# data = feature_collection.text
# feature = json.loads(data)
# '''
