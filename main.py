import requests
from lxml import html
from PIL import Image, ImageDraw, ImageFont, ImageOps,ImageEnhance
from io import BytesIO
import json
from flask import Flask, send_file

__version__ = '1.0.0'
app = Flask(__name__)

with open('lift_urls.json','r') as f:
    lift_urls = json.load(f)
    lift_status_urls = lift_urls["lift reports"]

def get_lifts(resort):

    if not resort in lift_status_urls:
        return None

    url = lift_status_urls[resort]

    page = requests.get(url)
    tree = html.fromstring(page.content)

    if resort == 'perisher':
        lift_statuses = tree.xpath("//table//tr//td//@title")
        lift_names = tree.xpath("//table//tr//td[2]//text()")
        lift_names = [l.split("(")[0].strip().lower() for l in lift_names if l != "Opens"]
        return zip(lift_names,lift_statuses)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

def get_img_coords(resort):
    with open('lift_image_coords.json','r') as f:
        coords = json.load(f)[resort]

    for lift in coords:
        coords[lift] = tuple(int(i) for i in coords[lift][1:-1].split(','))

    return coords

def get_trail_map_img(resort):

    trailmap = f'images/{resort}.jpg' 
    trailmap = Image.open(trailmap)
    
    return trailmap

    

def apply_lift_statuses(trail_map_img,coords,lifts):

    filter = ImageEnhance.Color(trail_map_img)
    trail_map_img = filter.enhance(.3)

    draw = ImageDraw.Draw(trail_map_img)

    for lift in lifts:

        if lift[1] == 'Open':
            draw.line(coords[lift[0]], fill='green', width = 10)

        elif lift[1] == 'Closed':
            draw.line(coords[lift[0]], fill='red', width = 10)

        elif lift[1] == 'On Standby' or lift[1] == 'On Demand':
            draw.line(coords[lift[0]], fill='blue', width = 10)

        elif lift[1] == 'On Hold':
            draw.line(coords[lift[0]], fill='orange', width = 10)
            
        else:
            print('unknown: ',lift)
    
    return trail_map_img

        
@app.route("/")
def get_version():
    return "COMP1710 WebApp Version "+__version__

@app.route("/<resort>")
def generate_map(resort):

    resort = str(resort)
    
    if resort in ['buller','hotham','falls','thredbo']:
        trail_map_img = get_trail_map_img(resort)
        
        return serve_pil_image(trail_map_img)

    elif resort in ['perisher']:

        lifts = get_lifts(resort)
        trail_map_img = get_trail_map_img(resort)
        coords = get_img_coords(resort)
        trail_map_img = apply_lift_statuses(trail_map_img,coords,lifts)

        return serve_pil_image(trail_map_img)
    

    elif resort == 'offseason':
        trail_map_img = get_trail_map_img("perisher_offseason")
        
        return serve_pil_image(trail_map_img)
        


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


