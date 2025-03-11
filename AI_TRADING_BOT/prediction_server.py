from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/predict/{price}")
def predict(price: float):
    predicted_price = price * 1.02  # Example: Increase price by 2%
    return {"Predicted Price": predicted_price}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
