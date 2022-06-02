from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Instantiate the app
app = FastAPI()
# Add CORS middleware - allows cross-origin requests, so that the frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"data": {"message": ["Hello World", "Ivan", "Teste"], "date": None}, "status": 200}

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000,debug=True)
 
# run from terminal:
# uvicorn my_server:app --host 127.0.0.1 --port 8080