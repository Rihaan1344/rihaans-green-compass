from PIL import Image, ImageDraw, ImageFont
import os

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

sname_centerx = x_center("Ficus Benghalensis L.", sname_font)
draw.text((sname_centerx, 75), "Ficus Benghalensis L.", font=sname_font, fill="black")

#cname y = bottom right y of sname, i.e, bbox[3], + some whitespace

sname_bbox = draw.textbbox((sname_centerx, 75), "Ficus Benghalensis L.", font = sname_font) #get textbox dimensions
cname_bbox = draw.textbbox((x_center("Indian Banyan", cname_font), sname_bbox[3] - 120), "Indian Banyan", font=cname_font)



draw.text((cname_bbox[0], cname_bbox[1]), "Indian Banyan", font=cname_font, fill="black")

#body

body_x = 550 #common x

#species
#species y = cname_bbox bottom right y + whitespace
species_y = cname_bbox[3] + 100 #unique y
sdimensions = (body_x, species_y)
sbbox = draw.textbbox(sdimensions, "Species: ", font = body_font)
draw.text(sdimensions, "Species: ", font = body_font, fill = "black") 

#genus
genus_y = sbbox[3] + 30
gdimensions = (body_x, genus_y)
gbbox = draw.textbbox(gdimensions, "Genus: ", font = body_font)
draw.text(gdimensions, "Genus: ", font = body_font, fill = "black")

#family

family_y = gbbox[3] + 37
fdimensions = (body_x, family_y)
fbbox = draw.textbbox(fdimensions, "Family: ", font = body_font)
draw.text(fdimensions, "Family: ", font = body_font, fill = "black")

#common name

common_name_y = fbbox[3] + 30
cndimensions = (body_x, common_name_y)
cnbbox = draw.textbbox(cndimensions, "Common Name:", font = body_font)
draw.text(cndimensions, "Common Name: ", font = body_font, fill = "black")


# Save image
path = os.path.join(os.getcwd(), "static", "poster.png")
img.save(path)