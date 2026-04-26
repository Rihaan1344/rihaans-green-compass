import requests as req
from dotenv import load_dotenv
import os
import qrcode

load_dotenv()

PLANT_API_KEY = os.getenv("PLANT_API_KEY")
TEMPLATE_API_KEY = os.getenv("TEMPLATE_API_KEY")

if not PLANT_API_KEY: raise ValueError("key not found bro. how lock open if not key?")

bark_filepath = input("Please enter file path for the image of the bark of the tree: ")
leaf_filepath = input("Please enter file path for the image of the leaf of the tree: ")

url = f"https://my-api.plantnet.org/v2/identify/all?api-key={PLANT_API_KEY}"

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
    best = result["results"][0]

species = best["species"]["scientificName"]
genus = best["species"]["genus"]["scientificName"]
family = best["species"]["family"]["scientificName"]

common_names = best["species"].get("commonNames", [])
common_name = common_names[0] if common_names else "N/A"


template_id = 'bc04434b-ef5a-407e-ab5a-7d681d3d03b4'

url = 'https://api.templated.io/v1/render'
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {TEMPLATE_API_KEY}'
}

data = {
  'template': template_id,
  'layers': {
    'species-placeholder' : {
       'text' : species
    },

    'genus-placeholder' : {
       'text' : genus
    },

    'family-placeholder' : {
       'text' : family
    },

    'common-names-placeholder' : {
       'text' : common_name
    },

    'common-name' : {
       'text' : common_name
    },
    
    'scientific-name' : {
       'text' : species
    }
    
  }
}

response = req.post(url, json=data, headers=headers)
result = response.json()

if response.status_code == 200:
  print('Render request accepted.')
else:
  print('Render request failed. Response code:', response.status_code)
  print(response.text)

print("-" * 20)

print("Species:", species)
print("Genus:", genus)
print("Family:", family)
print("Common name:", common_name)

data = result["url"]
qr = qrcode.make(data)
qr.save("poster_qr.png")

