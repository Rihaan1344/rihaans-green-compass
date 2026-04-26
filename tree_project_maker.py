import requests as req
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY: raise ValueError("key not found bro. how lock open if not key?")

bark_filepath = input("Please enter file path for the image of the bark of the tree: ")
leaf_filepath = input("Please enter file path for the image of the leaf of the tree: ")

url = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"

with open(bark_filepath, "rb") as bark, open(leaf_filepath, "rb") as leaf:
    files = [
        ("images", bark),
        ("images", leaf)
    ]
    data = {
    "organs": ["bark", "leaf"]
    }

    response = req.post(url, files=files, data=data)
    result = response.json()

   
if "results" not in result or not result["results"]:
    print("Could not identify, please try a clearer image")

else:
    best_match = result["bestMatch"]
    print("-" * 20)
    print("BEST MATCH: ", best_match)

    for r in result["results"]:
        species = r["species"]["scientificName"]
        genus = r["species"]["genus"]["scientificName"]
        family = r["species"]["family"]["scientificName"]
        score = r["score"]

        print("-" * 20)
        print(f"Score: {score}; {species} species, {genus} genus, {family} family.")

