import requests
from lxml import html
from PIL import Image, ImageDraw, ImageColor
from io import BytesIO
import os

coords = {"perisher quad express" : (1153,717,1129,1499),
"eyre t-bar" : (230,1087,563,657),
"international t-bar" : (374,1193,558,761),
"mt perisher double chair" : (587,1332,604,599),
"mt perisher triple chair" : (619,1328,636,657),
"sun valley t-bar" : (852,1021,683,836),
"olympic t-bar" : (791,766,1083,703),
"happy valley t-bar" : (731,1157,1129,916),
"leichhardt quad chair" : (753,1374,1044,1071),
"home rope tow" : (764,1401,929,1377),
"lawson t-bar" : (927,1462,1056,1096),
"blaxland t-bar": (957,1469,1239,1115),
"wentworth t-bar": (971,1481,1250,1125),
"quad express": (1130,1498,1153,717),
"sturt t-bar": (1150,1500,1298,1183),
"village 8 express chair" : (1281,1527,1379,1154),
"mitchell t-bar" : (1137,1514,1450,1209),
"tom thumb" : (1367,1514,1435,1475),
"telemark t-bar" : (1794,1502,1453,1292),
"pretty valley double chair" : (1785,1356,1161,862),
"north perisher t-bar" : (2224,1243,2149,968),
"interceptor quad chair" : (2118,1293,1911,930),
"ski carpet no. 1" : (1328,1508,1341,1469),
"ski carpet no. 2": (1351,1513,1374,1454),
"ski carpet no. 3": (1420,1509,1440,1480),
"ski carpet no. 4": (1420,1509,1440,1480), #I don't know where this is..?
"piper t-bar": (1827,1529,2118,1455),
"link t-bar": (2713,1644,2434,1347),
"burke t-bar": (2839,1629,2689,1227),
"wills t-bar": (2852,1625,2703,1223),
"kaaten triple chair": (2896,1635,2898,1266),
"hume t-bar": (2931,1627,2956,1206),
"captain cook j-bar": (3038,1618,3255,1380),
"scott j-bar": (3089,1622,3305,1488),
"zoe's ski carpet": (2773,1660,2725,1660),
"harry's & herman's ski carpet": (2826,1635,2781,1574),
"ridge quad chair": (2849,992,2641,447),
"summit quad chair": (2391,779,2569,386),
"pony ride carpet": (1837,738,1959,711),
"early starter double chair": (2249,723,2010,672),
"terminal quad chair": (2326,786,2004,708),
"brumby t-bar": (2168,893,2016,721),
"blue cow ski school rope tow": (1908,744,1964,729),
"pleasant valley quad chair": (2155,910,1353,706),
"freedom quad chair": (1549,625,2033,386),
"blue cow t-bar": (1717,503,2025,379),
"blue calf t-bar": (1375,577,1597,479),
"carpark double chair": (1758,467,1692,492),
"tube town": (1807,1659,1835,1593),
}

def lift_url(resort):
   return {'perisher' : r'https://www.perisher.com.au/reports-cams/reports/lift-report'}[resort]

def lift_map(resort):
    return {'perisher' : BytesIO(requests.get(r'https://www.perisher.com.au/images/trailmaps/2019/13362_PSR_FA2_WebsiteTrailMaps_May19_Perisher.jpg').content)}[resort]
    #return {'perisher' : r'D:\Projects\Python Programs\LiftStatusMaps\PerisherMap.jpg'}[resort]

def get_lifts(resort):

    url = lift_url(resort)

    page = requests.get(url)
    tree = html.fromstring(page.content)

    if resort == 'perisher':
        lift_statuses = tree.xpath("//table//tr//td//@title")
        lift_names = tree.xpath("//table//tr//td[2]//text()")
        lift_names = [l.split("(")[0].strip().lower() for l in lift_names if l != "Opens"]
        return zip(lift_names,lift_statuses)


resort = 'perisher'

lifts = get_lifts(resort)


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

    else:
        print('unknown: ',lift)

im.show()
