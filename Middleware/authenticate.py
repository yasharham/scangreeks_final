import re
from jose import jwt, JWTError
from fastapi import HTTPException, Security, Depends,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from passlib.exc import InvalidTokenError
from Services import schemas
import random,string



# ------------------------------------------------Token Generation ------------------------

SECRET_KEY = 'c5f2c18e0f38c757a0fc669730135fc60bd056c4dda4e4ee68d98cbb462bd842'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def email(email_id):
    """
    This function check an email format

    parameter
    ________

    :param email_id: str
                        Your email id
    :return: Boolean
    """
    format = "^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(format, email_id):
        return True
    return False


def generate_otp():
    otp = random.randint(100000, 999999)
    return otp


def create_access_token(data: dict, expires_delta: timedelta ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# -------------------------------Token Verification-----------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")
def decode_access_token(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username,role=role)
    except JWTError:
        raise credentials_exception
    return token_data

    # user = user_collection.find_one({'username':token_data.username})
    # if user is None:
    #     raise credentials_exception

# --------------------------------------------Authentication Password ----------------------------
class AuthHandler():
    """
    Authenticate handler
    ___________________

    """

    # security = HTTPBearer()
    pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")

    def get_pwd_hash(self, password):
        """
        This fuction convert plain password to hashed password

        Parameters
        __________

        :param password: str
                        Required param
        :return: str
                This fuction return hashed password
        """
        return self.pwd_cxt.hash(password)

    def verify_pwd(self, plain_pwd, hashed_pwd):
        """
        This function verify the password given plain password and store hashed password same or not

        Parameters
        __________

        :param plain_pwd: str
                            User's password
        :param hashed_pwd: str
                            User's hashed password
        :return: Boolean
        """
        return self.pwd_cxt.verify(plain_pwd, hashed_pwd)

    def encode_token(self, branch_id):
        """
        This function use for encode token using branch_id

        Parameters
        __________

        :param branch_id: str
                            Your branch_id
        :return: str
                    encrypted token
        """
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'branch_id': branch_id
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')


    def decode_token(self, token):
        """
        This function use for decryption of token

        Parameters
        __________

        :param token: str
                        encode token
        :return: str
                    branch_id
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            return payload['branch_id']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Invalid tokenn")

    # def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
    #     return self.decode_token(auth.credentials)







# s = AuthHandler()
# # pwd = generate_password(9)
# asd = s.get_pwd_hash('Hdel@500ta')
# print(f'str = Hdel@500ta  hash = {asd}')