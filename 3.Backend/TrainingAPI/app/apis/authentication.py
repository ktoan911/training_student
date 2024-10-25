import re

from argon2 import PasswordHasher
from sanic.response import json
from app.constants.mongodb_constants import MongoCollections

from sanic_security.exceptions import CredentialsError
from app.databases.mongodb import MongoDB
from app.utils.jwt_utils import generate_jwt
from sanic import Blueprint


password_hasher = PasswordHasher()
authen = Blueprint('authen_blueprint', url_prefix='/authen')
_db = MongoDB(collection_name=MongoCollections.users)

@authen.route('/register', methods={'POST'})
async def register(request):
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return json({"message": "Missing username or password"}, status=400)
    
    username=validate_username(data["username"])
    if _db.check_user_exist(username): 
        raise CredentialsError("An account with this username may already exist.", 409)
    password = password_hasher.hash(data["password"])

    print()

    try:
        _db.add_user(
            {
                "username": username,
                "password": password
            }
        )
    except Exception:
        raise CredentialsError("An error occurred while creating the account.", 500)
    return json({"message": "Account created successfully"}, status=201)

@authen.route('/login', methods={'POST'})
async def login(request):
    # lấy tài khoản mật khẩu từ request
    data = request.json
    
    if not data or "username" not in data or "password" not in data:
        return json({"message": "Missing username or password"}, status=400)
    
    username = data["username"]
    password = data["password"]

    account = _db.get_user_by_username(username)
    if not account:
        raise CredentialsError("An account with this username may not exist.", 404)

    try:
        password_hasher.verify(account["password"], password)
    except Exception:
        raise CredentialsError("Incorrect password.", 401)

    try:
        jwt = generate_jwt(
            username=username
        )
    except Exception:
        raise CredentialsError("An error occurred while generating the JWT.", 500)
    
    return json({"jwt": jwt}, status=200)



def validate_username(username: str) -> str:
    """
    Validates username format.

    Args:
        username (str): Username being validated.

    Returns:
        username

    Raises:
        CredentialsError
    """
    if not re.search(r"^[A-Za-z0-9_-]{3,32}$", username):
        raise CredentialsError(
            "Username must be between 3-32 characters and not contain any special characters other than _ or -.",
            400,
        )
    return username


def validate_password(password: str) -> str:
    """
    Validates password requirements.

    Args:
        password (str): Password being validated.

    Returns:
        password

    Raises:
        CredentialsError
    """
    if not re.search(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).*$", password):
        raise CredentialsError(
            "Password must contain one capital letter, one number, and one special character",
            400,
        )
    return password
