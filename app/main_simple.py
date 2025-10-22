"""
Minimal working version of HireOps to test basic functionality
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="HireOps - Recruitment Tracking System", version="1.0.0")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HireOps - Recruitment Tracking</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h3>🎉 HireOps - Recruitment Tracking System</h3>
                        </div>
                        <div class="card-body">
                            <div class="alert alert-success">
                                <h4>✅ Application Started Successfully!</h4>
                                <p>Your HireOps recruitment tracking system is now running.</p>
                            </div>
                            
                            <h5>📋 What's Available:</h5>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">✅ FastAPI Backend</li>
                                <li class="list-group-item">✅ Basic Web Interface</li>
                                <li class="list-group-item">✅ Bootstrap UI Framework</li>
                                <li class="list-group-item">⏳ Database Setup (Run seed_data.py)</li>
                                <li class="list-group-item">⏳ Authentication System</li>
                                <li class="list-group-item">⏳ Full Application Features</li>
                            </ul>
                            
                            <div class="mt-4">
                                <h5>🚀 Next Steps:</h5>
                                <ol>
                                    <li>Install missing dependencies: <code>pip install sqlmodel python-jose passlib</code></li>
                                    <li>Run database setup: <code>python seed_data.py</code></li>
                                    <li>Restart the application</li>
                                    <li>Login with: username=admin, password=admin123</li>
                                </ol>
                            </div>
                            
                            <div class="mt-4">
                                <h5>🔗 API Endpoints:</h5>
                                <ul>
                                    <li><a href="/health" class="btn btn-outline-primary btn-sm">Health Check</a></li>
                                    <li><a href="/docs" class="btn btn-outline-info btn-sm">API Documentation</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "HireOps is running"}

@app.get("/setup")
async def setup_guide():
    """Setup guide"""
    return {
        "message": "HireOps Setup Guide",
        "steps": [
            "1. Install dependencies: pip install sqlmodel python-jose passlib python-dotenv",
            "2. Run database setup: python seed_data.py", 
            "3. Restart application",
            "4. Access full application at /"
        ],
        "default_credentials": {
            "admin": {"username": "admin", "password": "admin123"},
            "recruiter": {"username": "alice_recruiter", "password": "password123"}
        }
    }

if __name__ == "__main__":
    import uvicorn
    # Start with port 8001 to avoid common conflicts
    for port in [8001, 8002, 8003, 8004, 8000]:
        try:
            print(f"🚀 Starting HireOps on port {port}...")
            print(f"🌐 Visit: http://localhost:{port}")
            uvicorn.run(app, host="0.0.0.0", port=port)
            break
        except OSError as e:
            if "address already in use" in str(e).lower() or "10048" in str(e):
                print(f"⚠️  Port {port} is in use, trying next port...")
                continue
            else:
                raise e
    else:
        print("❌ Could not find an available port. Please close other applications using ports 8000-8004.")
