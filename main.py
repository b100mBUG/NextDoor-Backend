from fastapi import FastAPI
from api.endpoints.users import router as users_router
from api.endpoints.apartments import router as apartments_router
from api.oauth.oauth import router as oauth_router


app = FastAPI()

app.include_router(oauth_router)
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(apartments_router, prefix="/apartment", tags=["apartment"])
