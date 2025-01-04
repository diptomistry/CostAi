from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import calculate_router

# Initialize FastAPI
app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include routes
app.include_router(calculate_router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Delivery Cost Calculator API"}
