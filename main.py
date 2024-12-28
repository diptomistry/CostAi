from fastapi import FastAPI
from routes import calculate_router

# Initialize FastAPI
app = FastAPI()

# Include routes
app.include_router(calculate_router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Delivery Cost Calculator API"}
