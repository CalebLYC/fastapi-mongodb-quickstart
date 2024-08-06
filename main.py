from fastapi import FastAPI

from controllers import auth_controller, role_controller, user_controller



#Créer l'application avec FastAPI
app = FastAPI(
    title="Fastapi with MongoDB quickstart",
    summary="A quickstart of a backend app using Fastapi and MongoDB.",
)


app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(role_controller.router)


#Endpoint racine
@app.get("/")
async def root():
    return {"message": "Fastapi with MongoDB database quickstart!"}