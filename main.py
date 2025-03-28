from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

@app.get("/")
async def test_server():
    return {"response": "Everything works fine"}

@app.get("/check-render")
async def test_render_server():
    url= "https://wildlife-tracker.onrender.com"
    
    try:
        response = requests.get(url)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

    return {"response": "Hello, Render works..."}
    


destination_url = "https://wildlife-tracker.onrender.com/gps_locations/"  # Change this to your target URL

@app.get("/proxy")
async def proxy_request(
    token: str = Query(..., description="Authentication token"),
    animal_number: str = Query(..., description="Animal number"),
    latitude: str = Query(..., description="Latitude"),
    longitude: str = Query(..., description="Longitude"),
):
    # Validate that all parameters are provided
    if not all([token, animal_number, latitude, longitude]):
        raise HTTPException(status_code=400, detail="Missing required query parameters")

    data = {
        "token": token,
        "animal_number": animal_number,
        "latitude": latitude,
        "longitude": longitude,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "token": token,
    }

    try:
        response = requests.post(destination_url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

    return {"status_code": response.status_code, "response": response.json()}
