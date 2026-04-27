import requests as req
from dotenv import load_dotenv
import os
import qrcode
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

#PREREQ -> FUNCTION FOR POSTERIZING THE OBTAINED DATA

#for checking if bbox is out of bounds:

def is_out_of_bounds(bbox, screen_dim):   
    x1, y1, x2, y2 = bbox
    width, height = screen_dim
    
    return (
        x1 < 0 or
        y1 < 0 or
        x2 > width or
        y2 > height
    )

def posterize(full_scientific_name: str, species: str, genus: str, family: str, common_name: str, bark_img, leaf_img):
    #create blank poster
    dimensions = (2245, 1587)
    img = Image.new("RGB", dimensions, color=(30, 30, 60))
    draw = ImageDraw.Draw(img)

    #fonts

    fonts_dir = os.path.join("/System", "Library", "Fonts")

    def get_font(fontname, size):
        font_path = os.path.join(fonts_dir, fontname)
        return ImageFont.truetype(font_path, size)

    sname_font = get_font("Supplemental/Futura.ttc", 120)
    cname_font = get_font("Noteworthy.ttc", 175)
    sname_font_small = get_font("Supplemental/Futura.ttc", 70)

    body_font = get_font("Supplemental/Hoefler Text.ttc", 90)

    body_font_small = get_font("Supplemental/Hoefler Text.ttc", 60)
    #load template

    template = Image.open(os.path.join(os.getcwd(), "static", "tree_template.png"))
    img.paste(template, (0, 0))

    #add text

    def x_center(text: str, font) -> int:
        bbox = draw.textbbox((0, 0), text, font = font) #get textbox dimensions
        width = bbox[2] - bbox[0] #upper left x value - lower right x value = width
        centered_x = (dimensions[0] - width) // 2 #screen width - text width / 2 = centered x val
        return centered_x

    sname_centerx = x_center(f"{full_scientific_name}", sname_font)


    #cname y = bottom right y of sname, i.e, bbox[3], + some whitespace

    sname_bbox = draw.textbbox((sname_centerx, 75), f"{full_scientific_name}", font = sname_font) #get textbox dimensions
    cname_bbox = draw.textbbox((x_center(f"{common_name}", cname_font), sname_bbox[3] - 120), "Indian Banyan", font=cname_font)

    if is_out_of_bounds(sname_bbox, dimensions):
        sname_bbox = draw.textbbox((sname_centerx, 75), f"{full_scientific_name}", font = (sname_font := sname_font_small)) 
        sname_centerx = x_center(f"{full_scientific_name}", sname_font)


    draw.text((sname_centerx, 75), f"{full_scientific_name}", font=sname_font, fill="black")

    draw.text((cname_bbox[0], cname_bbox[1]), f"{common_name}", font=cname_font, fill="black")

    #body

    body_x = 550 #common x

    #species
    #species y = cname_bbox bottom right y + whitespace

    species_y = cname_bbox[3] + 100 #unique y
    sdimensions = (body_x, species_y)
    sbbox = draw.textbbox(sdimensions, f"Species: {species}", font = body_font)
    if is_out_of_bounds(sbbox, dimensions):
        sbbox = draw.textbbox(sdimensions, f"Species: {species}", font = (body_font := body_font_small)) 
        
    draw.text(sdimensions, f"Species: {species}", font = body_font, fill = "black") 

    #genus
    genus_y = sbbox[3] + 30
    gdimensions = (body_x, genus_y)
    gbbox = draw.textbbox(gdimensions, f"Genus: {genus}", font = body_font)
    draw.text(gdimensions, f"Genus: {genus}", font = body_font, fill = "black")

    #family

    family_y = gbbox[3] + 37
    fdimensions = (body_x, family_y)
    fbbox = draw.textbbox(fdimensions, f"Family: {family}", font = body_font)
    draw.text(fdimensions, f"Family: {family}", font = body_font, fill = "black")

    #common name

    common_name_y = fbbox[3] + 30
    cndimensions = (body_x, common_name_y)
    draw.text(cndimensions, f"Common Name: {common_name}", font = body_font, fill = "black")

    #bark and leaf images
    pil_bark = Image.open(bark_img)
    pil_leaf = Image.open(leaf_img)
    
    pil_bark = pil_bark.resize((500, 500))
    pil_leaf = pil_leaf.resize((500, 500))

    img.paste(pil_bark, (550, 1000, 1050, 1500))    
    img.paste(pil_leaf, (1250, 1000, 1750, 1500))    

    # Save image
    path = os.path.join(os.getcwd(), "static", "poster.png")
    img.save(path)

    #return path
    return path


# STEP 1: LOAD API KEYS

load_dotenv()

PLANT_API_KEY = os.getenv("PLANT_API_KEY") or st.secrets["PLANT_API_KEY"]
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY") or st.secrers["IMAGE_API_KEY"]

if not PLANT_API_KEY: raise ValueError("key not found bro. how lock open if not key?")

#STEP 2: USE ST TO GET IMAGES

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

#STEP 3: SEND IMAGES TO PLANTNET API

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

   #STEP 4: PRINT OUT RESULTS
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

      #STEP 5: SEND URL TO POSTER GENERATOR

      st.divider()
      st.header("Poster")

      poster = posterize(species=species, 
                full_scientific_name=species, 
                family=family,
                genus=genus, 
                common_name=common_name,
                bark_img=bark,
                leaf_img=leaf)
      st.markdown("Poster generated.")
      
      url ="https://api.imgbb.com/1/upload"

      data = {
            "key": IMAGE_API_KEY
         }

      files = {
         "image": open(poster, "rb")
      }

      response = req.post(url, data = data, files=files)
      if response.status_code == 200:
         result = response.json()
         data = result["data"]["url"] 

         st.markdown("Sucessfully obtained image link")

         qr = qrcode.make(data)
         qr_path = os.path.join(os.getcwd(), "static", "poster_qrcode.png")
         qr.save(qr_path)

         st.markdown("QR Code generated!")
         st.image(qr_path)
         st.markdown("Scan the QR code to view your poster")
         st.caption(f"...or access it directly via ")
         st.link_button("this link.", data)

      else: print("Error.\n", response)

