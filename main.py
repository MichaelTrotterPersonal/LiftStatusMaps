import requests
from lxml import html
from PIL import Image
from io import BytesIO

def lift_url(resort):
   return {'perisher' : r'https://www.perisher.com.au/reports-cams/reports/lift-report'}[resort]

def lift_map(resort):
    #return {'perisher' : BytesIO(requests.get(r'https://www.perisher.com.au/images/trailmaps/2019/13362_PSR_FA2_WebsiteTrailMaps_May19_Perisher.jpg').content)}[resort]
    return {'perisher' : r'D:\Projects\Python Programs\LiftStatusMaps\PerisherMap.jpg'}[resort]
    
def get_lifts(resort):

    url = lift_url(resort)

    page = requests.get(url)
    tree = html.fromstring(page.content)

    if resort == 'perisher':
        lift_statuses = tree.xpath("//table//tr//td//@title")
        lift_names = tree.xpath("//table//tr//td[2]//text()")
        lift_names = [l.strip() for l in lift_names if l != "Opens"]
        
        return zip(lift_names,lift_statuses)


#stats = get_lifts('perisher')
trail_map = lift_map('perisher')

im = Image.open(trail_map)
im.show()
