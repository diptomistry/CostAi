from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes import calculate_router

# Initialize FastAPI
app = FastAPI()
# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cost-ai.vercel.app/", "https://www.yourdomain.com"],  # Replace with your domain
    #allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(calculate_router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Delivery Cost Calculator API"}
