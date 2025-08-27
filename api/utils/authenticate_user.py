from clerk_backend_api import Clerk
import os
import jwt
from jwt import PyJWKClient
from dotenv import load_dotenv
load_dotenv()

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")
print(f"Using CLERK_JWKS_URL: {CLERK_JWKS_URL}")
async def authenticate_user(jwt_token: str):
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
            return user
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None

if __name__ == "__main__":
    import asyncio

    test_token = "Bearer eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDIyMkFBQSIsImtpZCI6Imluc18zMWJHWFczTmZSZ3E4V0kxNTNFVElXeUdMNUIiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwOi8vbG9jYWxob3N0OjMwMDAiLCJjcmVhdGVkX2F0IjoxNzU2MTQ2MTQyLCJleHAiOjE3NTYzMDMzMjcsImZ1bGxfbmFtZSI6bnVsbCwiaWF0IjoxNzU2MzAzMjc2LCJpc3MiOiJodHRwczovL2V4YWN0LWdydWItMjEuY2xlcmsuYWNjb3VudHMuZGV2IiwianRpIjoiZjBlMTRlYjk3YWEyNjBmMTUwYWMiLCJuYmYiOjE3NTYzMDMyNzEsInByaW1hcnlfZW1haWwiOiJrYXVzMWtjMGRlc0BnbWFpbC5jb20iLCJzdWIiOiJ1c2VyXzMxbjNqSmE2OGpZZzV6UTRBOWVKTUUxMXVvZCIsInVzZXJfaWQiOiJ1c2VyXzMxbjNqSmE2OGpZZzV6UTRBOWVKTUUxMXVvZCJ9.O6GxP5nUkEhRELR7AGqRoWXvO6QBhFMNQHhfBBOkf6IjVLdVfxWYY1UWBHmrAsh6oHvUW49ZRPQn3da7pbRIXAQ6-LDOddoQ1-xsbfxl7Hzm-i04OUFxo7-fDsoj7x1nSUo20ajSTo-46iXnulqGM61ezLikh7XVELJWy9wCJ1uzoLN6_TBgEO7DipXR7pQGj54rfvp0qB3IdwcaDWRjUPJ6q6-lDmVsOWvn_oR04l9ntG2J9KRvV7KzoMJzyVZfq4FGazVqkqfamSMFTC_7zhs4eNNryi5oZBJocH5I7ZlIrJzTHeNHBTD7QAgWcxq_tCNmRaJqqJRFoF0TAaFRGg"
    token = test_token.split(" ")[1]
    user = asyncio.run(authenticate_user(token))
    print(type(user))
    with open("user.json", "w") as f:
        import json
        user_data = json.loads(user.model_dump_json())
        json.dump(user_data, f, indent=4)
        print(user_data)