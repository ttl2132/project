import requests
import pandas as pd
import uvicorn
from fastapi import FastAPI
from loguru import logger

# create the app as an instance of the fastAPI class
app = FastAPI(debug = True)
LB_URL = "https://raw.githubusercontent.com/ttl2132/ttl2132.github.io/master/data"

@app.get("/")
def landing_page():
    "Landing page for bio-minigame."
    return "Hi! You can find the leaderboard at this URL/scores"

@app.post("/scores/{initials}/{score}")
def update_scores(initials: str, score: str):
    "Checks and updates the leaderboard if a new score is a high score."
    return "posted"

@app.get("/scores")
def get_scores():
    "Gets the data from the URL and returns the information as a JSON."
    data = pd.read_csv(f"{LB_URL}/leaderboard.csv")
    logger.debug(data)
    return 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)