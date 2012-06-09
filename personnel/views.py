# Create your views here.
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from auxdb.personnel.models import Person

font = 'Times-Roman'

def side_draw(p,x,y,s):
    p.saveState()
    p.translate(x,y)
    p.rotate(-90)
    p.drawString(0,0,s)
    p.restoreState()

def fill_field(p, x, y, maxx, s):
    fontsize = 12
    max_width = maxx - x
    w = p.stringWidth(s, fontName=font, fontSize=fontsize)
    while w > max_width:
        fontsize -= 1
        w = p.stringWidth(s,font, fontsize)
    p.setFont(font, fontsize)
    p.drawString(x,y,s)


def aps1_pdf(request, pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')

    person = Person.objects.get(pk=pk)

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    p.drawImage('APS1-Front.tif', 0, 54, 72*8.5, 72*11)

    
    p.setFont(font, 12)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    fill_field(p, 54,729,205,person.last_name)
    fill_field(p,210,729,280,person.first_name)

    fill_field(p, 75,700,230,person.address)
    fill_field(p,252,700,280,person.apt)
    fill_field(p, 36,680,175,person.city)
    fill_field(p,180,680,235,person.state)
    fill_field(p,240,680,280,person.zipcode)

    fill_field(p, 75,648,280,person.verified)
    fill_field(p, 80,632,280,person.phone)
    fill_field(p, 90,615,205,person.birthplace)
    fill_field(p,100,596,280,person.birth_cert)
    fill_field(p,150,550,280,person.entry_port)
    fill_field(p,112,530,280,person.naturalize)
    fill_field(p,112,510,280,person.green_card)
    fill_field(p,112,492,280,person.other_proof)
    fill_field(p,115,472,280,str(person.warrant_date))
    fill_field(p,115,452,280,str(person.dmv_date))
    if person.gender == "M":
        fill_field(p,324,735,342,"X")
    if person.gender == "F":
        fill_field(p,360,735,378,"X")
    
    fill_field(p,440,735,560,person.marital)
    fill_field(p,332,712,360,person.height)
    fill_field(p,380,712,410,str(person.weight))
    fill_field(p,450,712,480,person.hair_color)
    fill_field(p,522,712,560,person.eye_color)
    fill_field(p,420,695,560,person.aka)
    if person.addicted:
        fill_field(p,370,665,410,"Yes")
    else:
        fill_field(p,370,665,410,"No")

    if person.mental:
        fill_field(p,486,665,560,"Yes")
    else:
        fill_field(p,486,665,560,"No")
        


    side_draw(p,582,612,person.last_name)
    side_draw(p,582,477,person.first_name)
    side_draw(p,582,324,str(person.idno))
    side_draw(p,582,171,'024')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


