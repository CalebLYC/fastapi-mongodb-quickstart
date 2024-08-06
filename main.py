from fastapi import FastAPI

from controllers import auth_controller, role_controller, user_controller



#Créer l'application avec FastAPI
app = FastAPI(
    title="EPL Concours API",
    summary="Application of the backend of admission to EPL.",
)


app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(role_controller.router)


#Endpoint racine
@app.get("/")
async def root():
    return {"message": "EPL Concours API!"}