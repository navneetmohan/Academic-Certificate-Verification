import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import init_db
from app.blockchain.client import blockchain_service
from app.api.auth import router as auth_router
from app.api.certificates import router as certificates_router
from app.api.verify import router as verify_router
from app.api.blockchain import router as blockchain_router
from app.api.stats import router as stats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database & load blockchain configuration
    print("[APP] Initializing database tables and seed data...")
    init_db()
    
    if blockchain_service.is_connected():
        print(f"[APP] Connected to Blockchain node at {blockchain_service.rpc_url}")
        print(f"[APP] Contract Address: {blockchain_service.contract_address or 'Pending Deployment'}")
    else:
        print(f"[APP] WARNING: Could not connect to blockchain at {blockchain_service.rpc_url}")
        
    yield
    print("[APP] Shutting down application...")

app = FastAPI(
    title="Blockchain-Based Academic Certificate Verification API",
    description="Decentralized hybrid on-chain/off-chain certificate verification service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers under /api
app.include_router(auth_router, prefix="/api")
app.include_router(certificates_router, prefix="/api")
app.include_router(verify_router, prefix="/api")
app.include_router(blockchain_router, prefix="/api")
app.include_router(stats_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "service": "Blockchain Academic Certificate Verification API",
        "status": "online",
        "blockchain_connected": blockchain_service.is_connected(),
        "contract_address": blockchain_service.contract_address or "Not Configured",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
