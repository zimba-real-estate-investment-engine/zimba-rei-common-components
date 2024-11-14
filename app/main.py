from fastapi import FastAPI
from app.core.database import engine, Base  # Import your SQLAlchemy Base and engine
from app.routes import users  # Import routes (users as an example)

# Create the FastAPI app
app = FastAPI()

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Include the routes
app.include_router(users.router, prefix="/users", tags=["Users"])

# Additional routes can be included as needed
# app.include_router(other_route.router, prefix="/other", tags=["Other"])
