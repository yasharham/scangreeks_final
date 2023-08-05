loginResponses = {
    200: {"status": "Success", 'status_code': 200, "message": "Login Successful"},
    401: {"status": "Unauthorized", 'status_code': 401,"message": "Invalid Credential"},
}

signUpResponse= {
    200: {"status": "success", 'status_code': 200, "message": "Signup Successful"},
    400: {"status": "bad request", 'status_code': 401, "message": "User Exist"},
    406: {"status": "not acceptable", 'status_code': 406, "message": "Invalid Email format"},
    413: {"status": "error", 'status_code': 413, "message": "Email already in use."}
}

response={
    200: {"status": "Success", 'status_code': 200, "message": "Fetched Successful"},
    401: {"status": "Unauthorized", 'status_code': 401,"message": "Login Required"},
    500: {"status": "Error", 'status_code': 500, "message": "Server Error... will update soon"}
}

