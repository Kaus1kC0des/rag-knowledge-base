from clerk_backend_api import Clerk
from jwt import PyJWKClient
from dotenv import load_dotenv
from api.models import UserModel
import os
import jwt
import warnings
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

warnings.filterwarnings("always")
load_dotenv()

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")
security = HTTPBearer()

async def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt_token = credentials.credentials
    clerk_api_key = os.getenv("CLERK_API_KEY")
    try:
        # Fetch JWKS and verify JWT
        jwks_client = PyJWKClient(CLERK_JWKS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(jwt_token)
        claims = jwt.decode(
            jwt_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=None,  # Set if you use audience
            options={"verify_exp": True}
        )
        user_id = claims.get("sub")
        async with Clerk(bearer_auth=os.getenv("CLERK_API_KEY")) as clerk:
            user = await clerk.users.get_async(user_id=user_id)
            user_id = user.id
            user_first_name = user.first_name
            user_last_name = user.last_name
            user_email_address = user.email_addresses[0].email_address
            return UserModel(id=user_id, first_name=user_first_name, last_name=user_last_name, email=user_email_address)
    except Exception as e:
        print(f"Authentication failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")