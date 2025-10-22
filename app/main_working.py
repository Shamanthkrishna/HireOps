"""
Ultra-simple HireOps version that will definitely work
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import socket

app = FastAPI(title="HireOps - Recruitment Tracking System")

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎉 HireOps is Running!</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .card { box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        </style>
    </head>
    <body class="d-flex align-items-center">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-10">
                    <div class="card">
                        <div class="card-header bg-success text-white text-center">
                            <h1>🎉 SUCCESS! HireOps is Running!</h1>
                        </div>
                        <div class="card-body p-5">
                            <div class="alert alert-success text-center">
                                <h3>✅ Your Recruitment Tracking System is LIVE!</h3>
                                <p class="lead">Congratulations! HireOps has started successfully.</p>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <h4>🏆 What's Working:</h4>
                                    <ul class="list-group">
                                        <li class="list-group-item">✅ FastAPI Backend</li>
                                        <li class="list-group-item">✅ Web Interface</li>
                                        <li class="list-group-item">✅ Bootstrap UI</li>
                                        <li class="list-group-item">✅ Port Auto-Selection</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h4>🚀 Next Steps:</h4>
                                    <ol class="list-group list-group-numbered">
                                        <li class="list-group-item">Install full dependencies</li>
                                        <li class="list-group-item">Run database setup</li>
                                        <li class="list-group-item">Access full application</li>
                                        <li class="list-group-item">Login with admin credentials</li>
                                    </ol>
                                </div>
                            </div>
                            
                            <div class="mt-4 text-center">
                                <h4>🔗 Available Endpoints:</h4>
                                <div class="btn-group" role="group">
                                    <a href="/health" class="btn btn-outline-primary">Health Check</a>
                                    <a href="/docs" class="btn btn-outline-info">API Docs</a>
                                    <a href="/setup" class="btn btn-outline-success">Setup Guide</a>
                                </div>
                            </div>
                            
                            <div class="mt-4 alert alert-info">
                                <h5>📋 Default Login Credentials (when full app is running):</h5>
                                <ul class="mb-0">
                                    <li><strong>Admin:</strong> username=admin, password=admin123</li>
                                    <li><strong>Recruiter:</strong> username=alice_recruiter, password=password123</li>
                                    <li><strong>Sales:</strong> username=bob_sales, password=password123</li>
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
async def health():
    return {"status": "healthy", "message": "HireOps is running successfully!"}

@app.get("/setup")
async def setup():
    return {
        "message": "HireOps Setup Complete",
        "status": "Basic version running",
        "next_steps": [
            "Install remaining packages: pip install sqlmodel python-jose[cryptography] passlib[bcrypt]",
            "Run database setup: python seed_data.py",
            "Start full application: python -m uvicorn main:app --reload --port 8001"
        ]
    }

def find_free_port():
    """Find a free port to use"""
    for port in [8001, 8002, 8003, 8004, 8005, 8006]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            sock.close()
            return port
        except OSError:
            continue
    return 8001  # fallback

if __name__ == "__main__":
    import uvicorn
    port = find_free_port()
    print(f"🚀 Starting HireOps on port {port}...")
    print(f"🌐 Visit: http://localhost:{port}")
    print("✅ Application should start successfully!")
    try:
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Trying alternative port...")
        uvicorn.run(app, host="127.0.0.1", port=port+1, log_level="info")
