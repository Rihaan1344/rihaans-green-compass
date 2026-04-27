import requests as req
from dotenv import load_dotenv
import os
import qrcode
import streamlit as st

load_dotenv()

PLANT_API_KEY = os.getenv("PLANT_API_KEY")
TEMPLATE_API_KEY = os.getenv("TEMPLATE_API_KEY")

if not PLANT_API_KEY or not TEMPLATE_API_KEY: raise ValueError("key not found bro. how lock open if not key?")

st.title("Rihaan's Green Compass")
st.markdown("Upload an image of the bark and the leaf, and you'll get a ready-made QR code which leads you to a beautiful green poster of the tree's scientific information!")
st.divider()
st.header("Upload images")

bark = st.file_uploader(
   "Upload an image of the bark of the tree",
   type = ["jpg", "png", "jpeg"]
)   

leaf = st.file_uploader(
   "Upload an image of the leaf of the tree",
   type = ["jpg", "png", "jpeg"]
)

st.divider()
if bark and leaf:
   url = f"https://my-api.plantnet.org/v2/identify/all?api-key={PLANT_API_KEY}"

   files = [
         ("images", bark.read()),
         ("images", leaf.read())
      ]
   data = {
      "organs": ["bark", "leaf"]
      }

   response = req.post(url, files=files, data=data)
   result = response.json()

   st.header("Plant classification")

      
   if "results" not in result or not result["results"]:
      msg = "Could not identify, please try a clearer image"
      print(msg)
      st.markdown(msg)

   else:
      best = result["results"][0]


      species = best["species"]["scientificName"]
      genus = best["species"]["genus"]["scientificName"]
      family = best["species"]["family"]["scientificName"]

      common_names = best["species"].get("commonNames", [])
      common_name = common_names[0] if common_names else "N/A"

      st.markdown(f"Species: {species}")
      st.markdown(f"Genus: {genus}")
      st.markdown(f"Family: {family}")
      st.markdown(f"Common Name: {common_name}")

      print("-" * 20)

      print("Species:", species)
      print("Genus:", genus)
      print("Family:", family)
      print("Common name:", common_name)

      st.divider()
      st.header("Poster QR code")

      template_id = "bc04434b-ef5a-407e-ab5a-7d681d3d03b4"

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


      if response.status_code == 200:
         msg = 'Render request accepted.'
         print(msg)
         st.markdown(msg)

         result = response.json()

         data = result["url"]
         qr = qrcode.make(data)
         path = os.path.join(os.getcwd(), "static", "poster_qr.png")
         qr.save(path)

         st.image(path)

         st.markdown("Scan the QR code to view your poster")
         st.caption(f"...or access it directly via ")
         st.link_button("this link.", data)

      else:
         msg = f'Render request failed. Response code: {response.status_code}'
         print(msg)
         print(response.text)

         st.markdown(msg)
         st.markdown(response.text)
