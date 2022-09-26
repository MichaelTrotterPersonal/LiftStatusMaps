import requests
from lxml import html
from PIL import Image, ImageDraw, ImageColor
from io import BytesIO, StringIO
import os
import json
from flask import Flask, send_file
__version__ = '1.0.0'
app = Flask(__name__)

def lift_url(resort):
   return {'perisher' : r'https://www.perisher.com.au/reports-cams/reports/lift-report'}[resort]

def lift_map(resort):
    return {'perisher' : BytesIO(requests.get(r'https://www.perisher.com.au/images/trailmaps/2019/13362_PSR_FA2_WebsiteTrailMaps_May19_Perisher.jpg').content)}[resort]

def get_lifts(resort):

    url = lift_url(resort)

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

@app.route("/")
def get_version():
    return "COMP1710 WebApp Version "+__version__

@app.route("/<resort>")
def generate_map(resort):
    resort = str(resort)

    lifts = get_lifts(resort)
    
    with open('lift_image_coords.json','r') as f:
        coords = json.load(f)[resort]

    for lift in coords:
        coords[lift] = tuple(int(i) for i in coords[lift][1:-1].split(','))

    trailmap = resort + 'MapBW.jpg' 

    if not os.path.isfile(trailmap):
        im = Image.open(lift_map(resort))
        im = im.convert('L') # convert image to black and white
        im.save(resort + 'MapBW.jpg')
    else:
        print('trailmap found in folder')

    
    im = Image.open(trailmap)

    im = im.convert('RGB')
    draw = ImageDraw.Draw(im)

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
    
    return serve_pil_image(im)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)