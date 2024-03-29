from cassettes.construct.models import Cassette,CassetteAssembly, Modulemap,Step
import csv

types = {
    "FI": {
        "pg": "-0.01,-96.71, 83.69,-48.31, 83.69,48.29, -0.01,96.69, -83.71,48.29, -83.71,-48.31",
        "roff": 0,
        "nROCs": 6,
        "den": 'HD',
        "fill": "rgb(180,180,0)"
    },
    "gI": {
        "pg": "0.02,96.7, -24.58,82.5, -24.58,-82.5, 0.02,-96.7, 83.72,-48.3, 83.72,48.3",
        "roff": 3,
        "style": "stroke:black;stroke-width:10;",
        "nROCs": 6,
        "den": 'HD',
        "fill": "rgb(180, 150, 0)"
    },
    "dI": {
        "pg": "0.04,96.69, -24.56,82.49, 59.14,-62.51, 83.74,-48.31, 83.74,48.29",
        "roff": 3,
        "style": "stroke:black;stroke-width:10;",
        "nROCs": 3,
        "den": 'HD',
        "fill": "rgb(180, 150, 0)"
    },
    "aI": {
        "pg": "-83.68,-48.35, 83.72,48.35, 0.02,96.65, -83.68,48.35",
        "roff": 1,
        "style": "stroke:black;stroke-width:10;",
        "nROCs": 6,
        "den": 'HD',
        "fill": "rgb(180, 150, 0)"
    },
    "bI": {
        "pg": "-83.7,-48.29, 83.7,-48.29, 83.7,48.31, 0,96.71, -83.7,48.31, -83.7,-48.2",
        "roff": 1,
        "style": "stroke:black;stroke-width:10;",
        "nROCs": 6,
        "den": 'HD',
        "fill": "rgb(180, 150, 0)"
    },
    "FM": {
        "pg": "-0.01,-96.71, 83.69,-48.31, 83.69,48.29, -0.01,96.69, -83.71,48.29, -83.71,-48.31",
        "roff": 0,
        "style": "stroke:purple;stroke-width:4;",
        "den": 'LD',
        "nROCs": 3,
        "fill": "rgb(220,220,0)"
    },
     "FO": {
        "pg": "-0.01,-96.71, 83.69,-48.31, 83.69,48.29, -0.01,96.69, -83.71,48.29, -83.71,-48.31",
        "roff": 0,
        "den": "LD",
        "nROCs": 3,
        "style": "stroke:purple;stroke-width:2;",
        "fill": "rgb(255,255,0)"
    },
    "FOe": {
        "pg": "-0.05,-96.71, 83.75,-48.31, 83.75,48.29, -0.05,96.69, -83.75,48.29, -83.75,-48.31",
        "roff": 0,
        "style": "stroke:purple;stroke-width:2;",
        "den": "LD",
        "nROCs": 3,
        "fill": "rgb(180, 150, 0)"
    },
    "aO": {
        "pg": "-0.05,-96.62, -0.05,96.68, -83.75,48.38, -83.75,-48.32, -0.05,-96.62",
        "roff": 0,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
    "bO": {
        "pg": "83.7,48.35, -83.7,48.35, -83.7,-48.36, 0,-96.66, 83.7,-48.36",
        "roff": 4,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
    "cO": {
        "pg": "-83.77,-48.3, 0.03,96.7, -83.77,48.3",
        "roff": 1,
        "nROCs": 1,
        "style": "stroke:purple;stroke-width:2;",
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
    "dO": {
        "pg": "-0.01,-96.64, 41.89,-72.54, -41.91,72.46, -83.71,48.36, -83.71,-48.3",
        "roff": 0,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 2,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
    "aM": {
        "pg": "-83.68,48.31, 83.72,-48.29, 83.72,48.31, 0.02,96.71",
        "roff": 2,
        "nROCs": 3,
        "den": "LD",
        "style": "stroke:purple;stroke-width:2;",
        "fill": "rgb(180, 150, 0)"
    },
    "bM": {
        "pg": "-83.7,48.32, 0,-96.68, 83.7,-48.38, 83.7,48.32, 0,96.72",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
    "other": {
        "pg": "",
        "roff": 0,
        "style": "stroke:purple;stroke-width:4;",
        "nROCs": 0,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
    "WAG": {
        "pg": "53.299999,-3.000000,163.139999,-3.000000,173.539993, 6.760000,193.539993, 6.760000,203.940002,-3.000000,220.740005,-3.000000,220.740005,-43.000000,163.139999,-43.000000,53.299999,-43.000000,-65.699997,-43.000000,-65.699997,-32.200001,-69.080002,-27.000000,-69.080002,-19.000000,-65.699997,-13.800000,-65.699997,-3.000000,-51.383999,-3.000000,19.830999,120.348000,48.631001,170.231003,83.272003,150.231003,86.524002,136.345001,76.524002,119.024002,62.872002,114.897003,54.472000,100.348000,-5.196000,-3.000000,-4.300000,-3.000000,6.100000,6.760000,26.100000,6.760000,36.500000,-3.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"DepDCDC": {
        "pg": "56.000000,-45.500000,56.000000,-60.400002,9.000000,-88.000000,-9.000000,-88.000000,-56.000000,-60.400002,-56.000000,-45.500000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"East1": {
        "pg": "53.299999,-3.000000,53.299999,-43.00000,65.699997,-43.00000,65.699997,-32.20000,69.080002,-27.00000,69.080002,-19.00000,65.699997,-13.80000,65.699997,-3.000000,-4.300000,-3.000000,6.100000,6.760000,26.100000,6.760000,36.500000,-3.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"East2": {
        "pg": "220.740005,-3.000000,220.740005,-43.000000,163.139999,-43.000000,53.299999,-43.000000,-65.699997,-43.000000,-65.699997,-32.200001,-69.080002,-27.000000,-69.080002,-19.000000,-65.699997,-13.800000,-65.699997,-3.000000,-4.300000,-3.000000,6.100000, 6.760000,26.100000, 6.760000,36.500000,-3.000000,53.299999,-3.000000,163.139999,-3.000000,173.539993,6.760000,193.539993,6.760000,203.940002,-3.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"East3": {
        "pg": "53.299999,-3.000000,163.139999,-3.000000,173.539993,6.760000,193.539993,6.760000,203.940002,-3.000000,220.740005,-3.000000,330.579987,-3.000000,340.980011, 6.760000,360.980011, 6.760000,371.380005,-3.000000,388.179993,-3.000000,388.179993,43.000000,330.579987,-43.000000,220.740005,-43.000000,163.139999,-43.000000,53.299999,-43.000000,-65.699997,-43.000000,-65.699997,-32.200001,-69.080002,-27.000000,-69.080002,-19.000000,-65.699997,-13.800000,-65.699997,-3.000000,-4.300000,-3.000000,6.100000,6.760000,26.100000,6.760000,36.500000,-3.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"EastTriangle": {
        "pg": "53.299999,-3.000000,163.139999,-3.000000,173.539993,6.760000,193.539993,6.760000,203.940002,-3.000000,220.740005,-3.000000,220.740005,-43.000000,163.139999,-43.000000,53.299999,-43.000000,-65.699997,-43.000000,-65.699997,-32.200001,-69.080002,-27.000000,-69.080002,-19.000000,-65.699997,-13.800000,-65.699997,-3.000000,-51.383999,-3.000000,19.830999,120.348000,48.631001,170.231003,83.272003,150.231003,86.524002,136.345001,76.524002,119.024002,62.872002,114.897003,54.472000,100.348000,-5.196000,-3.000000,-4.300000,-3.000000,6.100000,6.760000,26.100000,6.760000,36.500000,-3.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"HDEngine_East": {
        "pg": "52.220001,19.164000,83.220001,19.164000,93.220001,29.164000,103.720001,29.164000,113.720001,19.164000,115.720001,19.164000,127.720001,7.164000,127.720001,-32.835999,115.720001,-44.835999,91.720001,-44.835999,87.220001,-40.335999,81.220001,-40.335999,76.720001,-44.835999,62.720001,-44.835999,50.720001,-51.835999,55.720001,-60.835999,41.720001,-68.835999,29.719999,-56.835999,29.719999,-51.835999,20.719999,-42.835999,34.220001,-29.336000,41.720001,-36.835999,46.720001,-36.835999,52.220001,-31.336000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"HDEngine_West": {
        "pg": "52.220001,19.164000,83.220001,19.164000,93.220001,29.164000,103.720001,29.164000,113.720001,19.164000,115.720001,19.164000,127.720001,7.164000,127.720001,-32.835999,115.720001,-44.835999,91.720001,-44.835999,87.220001,-40.335999,81.220001,-40.335999,76.720001,-44.835999,62.720001,-44.835999,50.720001,-51.835999,55.720001,-60.835999,41.720001,-68.835999,29.719999,-56.835999,29.719999,-51.835999,20.719999,-42.835999,34.220001,-29.336000,41.720001,-36.835999,46.720001,-36.835999,52.220001,-31.336000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"LDEngine_East": {
        "pg": "-124.69999,-7.50000,-114.69999,-7.50000,-104.69999,2.50000,-56.700001,2.500000,-46.700001,-7.500000,-41.700001,-7.500000,-41.700001,-22.500000,-59.700001,-42.500000,-59.700001,-45.000000,-64.699997,-55.000000,-69.699997,-55.000000,-69.699997,-40.000000,-99.699997,-40.000000,-99.699997,-56.000000,-106.69999,-60.00000,-112.69999,-60.00000,-112.69999,-42.00000,-124.69999,-25.00000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"LDEngine_West": {
        "pg": "41.700001,-7.500000,51.700001,-7.500000,61.700001,2.500000,109.699997,2.500000,119.699997,-7.500000,124.699997,-7.500000,124.699997,-22.500000,106.699997,-42.500000,106.699997,-45.000000,101.699997,-55.000000,96.699997,-55.000000,96.699997,-40.000000,66.699997,-40.000000,66.699997,-56.000000,59.700001,-60.000000,53.700001,-60.000000,53.700001,-42.000000,41.700001,-25.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"West1": {
        "pg": "65.699997,-3.000000,65.699997,-13.800000,69.080002,-19.000000,69.080002,-27.000000,65.699997,-32.200001,65.699997,-43.000000,-4.300000,-43.000000,-4.300000,-3.000000,6.100000,6.760000,26.100000,6.760000,36.500000,-3.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"West2": {
        "pg": "65.699997, -3.000000,65.699997,-13.800000,69.080002,-19.000000,69.080002,-27.000000,65.699997,-32.200001,65.699997,-43.000000,-4.300000,-43.000000,-114.139999,-43.00000,-171.740005,-43.00000,-171.740005,-3.00000,-161.339996,6.76000,-141.339996,6.76000,-130.940002,-3.00000,-114.139999,-3.00000,-4.300000,-3.000000,6.100000,6.760000,26.100000,6.760000,36.500000,-3.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"West3": {
        "pg": "65.699997,-3.000000,65.699997,-13.800000,69.080002,-19.000000,69.080002,-27.000000,65.699997,-32.200001,65.699997,-43.000000,-4.300000,-43.000000,101.739998,-43.00000,171.740005,-43.00000,269.179993,-43.00000,339.179993,-43.00000,339.179993,-3.00000,328.779999,6.76000,308.779999,6.76000,298.380005,-3.00000,269.179993,-3.00000,171.740005,-3.00000,161.339996, 6.76000,141.339996, 6.76000,130.940002,-3.00000,101.739998,-3.00000,-4.300000,-3.000000,6.100000, 6.760000,26.100000, 6.760000,36.500000,-3.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
"WestHockey": {
        "pg": "65.699997,-3.000000,65.699997,-13.800000,69.080002,-19.000000,69.080002,-27.000000,65.699997,-32.200001,65.699997,-43.000000,-4.300000,-43.000000,-4.300000,-3.000000,19.830999,120.348000,48.631001,170.231003,103.551003,265.355011,132.350998,315.238007,166.992004,295.238007,170.244003,281.351990,160.244003,264.031006,146.591995,259.904999,138.192001,245.354996,83.272003,150.231003,86.524002,136.345001,76.524002,119.024002,62.872002,114.897003,54.472000,100.348000,36.500000,-3.000000",
        "roff": 2,
        "style": "stroke:purple;stroke-width:2;",
        "nROCs": 3,
        "den": "LD",
        "fill": "rgb(180, 150, 0)"
    },
}



types['dIe']=types['dI'];	      
types['gIe']=types['gI'];	      
types['bOe']=types['bO'];	      
types['cOe']=types['cO'];	      
types['aOeT']=types['aO'];	      
types['aOe']=types['aO'];	      
types['aMe']=types['aM'];	      
types['aMeT']=types['aM'];	      
types['aMeB']=types['aM'];	      
types['bMe']=types['bM'];	      
types['FMe']=types['FM'];	      
types['aIe']=types['aI'];	      
types['aOeB']=types['aO'];	      
types['dOe']=types['dO'];	
types['dOeL']=types['dO'];	
types['dOeR']=types['dO'];	
types['FIe']=types['FI'];	  



def upload_csv_to_model(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        headers = next(reader)  # Read the header row
        for row in reader:
            data = dict(zip(headers, row))
            mymodel = Modulemap(**data)  # Create a new instance of the model       
            mymodel.save()  # Save the model to the database


def generate_svg(parent_id):
    #assembly = CassetteAssembly.objects.get(pk=parent_id)
    # if not cassette.started:
    #     #upload_csv_to_model('cassettes/construct/modulemapper_geometry.hgcal.txt')
    #     cassette.started = True
    #     cassette.save()
    #step = Step.objects.get(pk=cassette.step)
    #layer = str(int(cassette.name.replace('CEE',''))*2 + int(cassette.side) - 2)
    # remove cassette.side for now
    #
    num = 0
    shapes = CassetteAssembly.objects.filter(layer=parent_id)
    svgstring = '<svg id=\'svg-assembly\' height=\'600\' width=\'700\'>\n'
    svgstring+='<defs>\n'
    svgstring+=' <marker id="arrowMarker" markerWidth="20" markerHeight="20" refX="18" refY="10" orient="auto" markerUnits="userSpaceOnUse">\n'
    svgstring+='  <polygon points="0,0 16,10 0,20" style="fill: black;" /> \n'
    svgstring+='</marker>\n'
    svgstring+='</defs>\n'
    # if (int(cassette.side)==1 ): 
    svgstring += '<g transform =\"translate(30,510) scale(0.4,-0.4) rotate(%s,0,0)\">\n' % (str(0))
    # else: 
    #     svgstring += '<g transform =\"translate(30,510) scale(0.4,0.4) rotate(%s,0,0)\">\n' % (str(-60))       
    for shape in shapes:
            # part, _ = Part.objects.get_or_create(module=shape)
            active = False
            if (shape.step.parts == types[shape.module.itype]["den"]): active = True
            numbers = [float(i) for i in types[shape.module.itype]["pg"].split(',')]
            totalrot = 60*float(types[shape.module.itype]["roff"]) + 60*float(shape.module.irot)
            trans = 'translate(%s, %s) rotate(%d, 0, 0)' % (shape.module.x0,shape.module.y0,totalrot)

            cenx = float(shape.module.x0)
            ceny = float(shape.module.y0)
            fill = types[shape.module.itype]["fill"]
            opacity = 0.3
            if shape.placed == True:
                fill = "rgb(0, 0, 255)"
                opacity = 0.3
            if not active:
                 fill = "rgb(200, 200, 200)"
            if active:
                 num+=1
            hexagon = '<polygon uv=\"u%sv%s\" points=\"%s\" fill=\"%s\" type=\"%s\" placed=\"%s\" id=\"%s\" barcode=\"%s\" active=\"%s\" transform=\"%s\" style=\'stroke:black;stroke-width:2\' opacity=\"%s\", onmouseover=\"ModMouseOver(this.id);\", onmouseout=\"ModMouseOut(this.id);\", onclick=\"ModOnClick(this.id);\") /> \n' % (shape.module.u,shape.module.v,types[shape.module.itype]["pg"],fill,shape.module.itype, shape.placed, shape.pk, shape.barcode, str(active).lower(), trans, opacity)      
            digit = '<text id="text%s\" x=0 y=0 transform=\"translate(%s, %s) rotate(%d, 0, 0) scale(-1,1)\" text-anchor="middle" alignment-baseline="middle" dominant-baseline="middle" fill="black" font-size="35px">%s</text> \n' % (num, cenx, ceny, 180, num)
            arrow = '<line id="arrow%s\" x1="0" y1="30" x2="0" y2="80" style="stroke: black; stroke-width: 6; marker-end: url(#arrowMarker);" transform=\"%s\" display="none"/> \n' % (shape.pk, trans)
            #hexagon = '<polygon uv=\"u%sv%s\" points=\"%s\" fill=\"%s\" type=\"%s\" placed=\"%s\" id=\"%s\" barcode=\"%s\" active=\"%s\" transform=\"%s\" style=\'stroke:black;stroke-width:2\' opacity=\"%s\") /> \n' % (shape.module.u,shape.module.v,types[shape.module.itype]["pg"],fill,shape.module.itype, shape.placed, shape.pk, shape.barcode, str(active).lower(), trans, opacity)                  
            svgstring+=hexagon
            if active:
                 svgstring+=digit
                 svgstring+=arrow
  
    svgstring+='<polyline id=\'Xaxis\'  points=\'0,0 1700,0\' style=\'stroke:black;stroke-width:1\' /><polyline  points=\'0,0 849.53,1472.48\' style=\'stroke:black;stroke-width:1\' />\n'
    svgstring+='</g>\n'
    svgstring+='</svg>'

    return svgstring


