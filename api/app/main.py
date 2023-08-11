from fastapi import FastAPI


app = FastAPI()


#Create Endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}