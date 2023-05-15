from django.shortcuts import render
from django.http import FileResponse,HttpResponse
from svgwrite import *
from construct.models import Cassette_test,Module_test



# Create your views here.

def myView(request):
  return render(request, "construct/svg.html")


def generate_svg(request, parent_id):
    # Get all the shapes for the parent object

    shapes = Module_test.objects.filter(cassette=parent_id)

    dwg = Drawing('assembly_diagram.svg', profile='full', size = ('50%','50%') )
    g = dwg.g(transform="translate(50,400) scale(1 -1) scale(0.5)")
    tempx = -999

    for shape in shapes:
        if (tempx==shape.u):
            shape.u+=0.5
            shape.v-=0.25

        if shape.type == 'square':
            x = shape.u - (shape.width / 2)
            y = shape.v - (shape.height / 2)
            square = dwg.rect(insert=(x, y), size=(shape.width, shape.height), fill='green')
            square['data-serial-number'] = shape.id
            square['data-type'] = shape.type
            square['data-coordinates'] = f"{x},{y},{x + shape.width},{y + shape.height}"
            dwg.add(square)
        elif (shape.type == 'HD' or shape.type == 'LD'):
            if shape.type == 'HD':
                color = 'purple'
            if shape.type == 'LD':
                color = 'blue'
            rotate = 'rotate(90,%s, %s)' % (100*shape.u,100*shape.v)
            side_length = 50
            height = side_length
            x1 = 100*shape.u - side_length
            x2 = 100*shape.u - side_length / 2
            x3 = 100*shape.u + side_length / 2
            x4 = 100*shape.u + side_length
            y2 = 100*shape.v
            y1 = 100*shape.v - height 
            y3 = 100*shape.v + height 

            points = [(x1,y2), (x2,y1),(x3,y1),(x4,y2),(x3,y3),(x2,y3) ]

            hexagon = dwg.polygon(points=points, fill=color,transform=rotate, style='stroke:black;stroke-width:5;', opacity = '0.6')
            # hexagon.set_desc('data-sn',shape.id)
            # hexagon.set_desc('data-modtype',shape.type)
            # hexagon.set_desc('data-id',"u"+str(shape.u)+"v"+str(shape.v))
            # hexagon.update({'sn': '0104', 'id': 'u1v5'})
            print (hexagon)
            g.add(hexagon)
            dwg.add(g)
            tempx=shape.u

    dwg.save()

    #Return the SVG as a string
    # response = HttpResponse(content_type='image/svg+xml')
    # response['Content-Disposition'] = f'attachment; filename="assembly_diagram.svg"'
    # response.write(dwg.tostring())
    # return response
    return FileResponse(open('assembly_diagram.svg', 'rb'))