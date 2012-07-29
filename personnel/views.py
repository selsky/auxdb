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

def calc_width(p,s,fontsize):
    words = s.split(' ')
    spaces = len(words) - 1
    width = 0.25*fontsize*spaces
    for word in words:
        width += p.stringWidth(word, fontName=font, fontSize=fontsize)
    return width

def print_string(p, x0, y, s, fontsize):
    x = x0 
    p.setFont(font, fontsize)
    words = s.split(' ')

    for word in words:
        p.drawString(x, y, word)
        x += p.stringWidth(word, fontName=font, fontSize=fontsize) + 0.25*fontsize
    

def fill_field(p, x, y, maxx, s):
    fontsize = 12
    max_width = maxx - x
    w = calc_width(p, s, fontsize)
    while w > max_width:
        fontsize -= 1
        w = calc_width(p, s, fontsize)
    print_string(p, x, y, s, fontsize)


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
        
    fill_field(p,390,648,560,person.marks)
    fill_field(p,390,630,560,person.defects)
    fill_field(p,370,610,560,person.ssn)
    fill_field(p,350,592,560,person.drivers)
    fill_field(p,350,572,468,person.pistol)
    fill_field(p,500,572,560,person.pistol_type)
    fill_field(p,350,552,414,person.draft_status)
    fill_field(p,480,552,560,person.discharge)
    fill_field(p,370,535,560,person.branch)

    if person.applied:
        fill_field(p,465,505,560,"Yes")
    else:
        fill_field(p,465,505,560,"No")

    if person.summonsed:
        fill_field(p,490,486,560,"Yes")
    else:
        fill_field(p,490,486,560,"No")

    fill_field(p,170,435,252,person.max_grade)
    fill_field(p,290,435,414,person.school)
    fill_field(p,460,435,560,person.location)

    fill_field(p, 36,420,212,person.emploer)
    fill_field(p,220,420,372,person.emp_address)
    fill_field(p,380,420,456,person.occupation)
    fill_field(p,464,420,522,person.emp_phone)
    fill_field(p,530,420,560,person.emp_length)

    fill_field(p,200,394,360,person.next_kin)
    fill_field(p,414,394,560,person.kin_relate)
    
    fill_field(p, 81,376,360,person.kin_addr)
    fill_field(p,414,376,560,person.kin_phone)
    
    side_draw(p,582,612,person.last_name)
    side_draw(p,582,477,person.first_name)
    side_draw(p,582,324,str(person.idno))
    side_draw(p,582,171,'024')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


