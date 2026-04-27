from PIL import Image, ImageDraw, ImageFont
import requests
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

API_KEY = os.getenv("IMAGE_API_KEY")
if not API_KEY: raise ValueError("Key not found.")

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

    body_font = get_font("Supplemental/Hoefler Text.ttc", 90)

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
    draw.text((sname_centerx, 75), f"{full_scientific_name}", font=sname_font, fill="black")

    #cname y = bottom right y of sname, i.e, bbox[3], + some whitespace

    sname_bbox = draw.textbbox((sname_centerx, 75), f"{full_scientific_name}", font = sname_font) #get textbox dimensions
    cname_bbox = draw.textbbox((x_center(f"{common_name}", cname_font), sname_bbox[3] - 120), "Indian Banyan", font=cname_font)



    draw.text((cname_bbox[0], cname_bbox[1]), f"{common_name}", font=cname_font, fill="black")

    #body

    body_x = 550 #common x

    #species
    #species y = cname_bbox bottom right y + whitespace
    species_y = cname_bbox[3] + 100 #unique y
    sdimensions = (body_x, species_y)
    sbbox = draw.textbbox(sdimensions, f"Species: {species}", font = body_font)
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
if leaf and bark:
    posterize("Ficus Benghalensis L", "F. benghalensis", "Ficus", "Moraceae", "Indian Banyan", bark, leaf)


""" image_path = os.path.join(os.getcwd(), "static", "test2_bark.jpeg")
url ="https://api.imgbb.com/1/upload"

data = {
        "key": API_KEY
    }

files = {
    "image": open(image_path, "rb")
}

response = requests.post(url, data = data, files=files)
if response.status_code == 200:
    result = response.json()
    print(result["data"]["url"])

else: print(response) """
    