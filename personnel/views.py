# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from reportlab.pdfgen import canvas
from auxdb.personnel.models import Person,Tour
from django.shortcuts import render, render_to_response
import datetime
from django.forms.models import modelformset_factory
from django.template import RequestContext
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
    fill_field(p,235,615,280,str(person.birth_date))
    fill_field(p,100,596,280,person.birth_cert)
    fill_field(p,112,578,280,"N/A")
    fill_field(p,150,550,280,person.entry_port)
    fill_field(p,112,530,280,person.naturalize)
    fill_field(p,112,510,280,person.green_card)
    fill_field(p,112,492,280,person.other_proof)
    fill_field(p,115,472,280,str(person.warrant_date))
    fill_field(p,115,452,280,str(person.dmv_date))
    if person.gender == "M":
        fill_field(p,324,730,342,"X")
    if person.gender == "F":
        fill_field(p,360,730,378,"X")
    
    fill_field(p,440,730,560,person.get_marital_display())
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

    fill_field(p, 36,420,212,person.employer)
    fill_field(p,220,420,372,person.emp_address)
    fill_field(p,380,420,456,person.occupation)
    fill_field(p,464,420,522,person.emp_phone)
    fill_field(p,530,420,560,person.emp_length)

    fill_field(p,200,394,360,person.next_kin)
    fill_field(p,414,394,560,person.kin_relate)
    
    fill_field(p, 81,376,360,person.kin_addr)
    fill_field(p,414,376,560,person.kin_phone)

    # FIXME: hack.  But a handy one right now.
    fill_field(p,110,90,280,"13MN01")
    
    side_draw(p,582,612,person.last_name)
    side_draw(p,582,518,person.first_name)
    side_draw(p,582,400,person.middle_name)
    side_draw(p,582,324,str(person.idno))
    side_draw(p,582,171,'024')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def fy_label (d):
    y = d.year
    if d.month <= 6:
        return "{0}-{1}".format(y-1,y)
    else:
        return "{0}-{1}".format(y,y+1)

def fy_range (d): 
    y = d.year
    if d.month <= 6:
        return (datetime.date(y-1,7,1),datetime.date(y,6,30))
    else:
        return (datetime.date(y,7,1),datetime.date(y+1,6,30))

def aps11_html(request, pk, fy):
    year = int(fy)
    person = Person.objects.get(pk=pk)
    date_min = datetime.date(year - 1,7,1)
    date_max = datetime.date(year,6,30)

    ord_min = date_min.toordinal()
    ord_max = date_max.toordinal()

    q = Tour.objects.filter(person__exact=person)
    q = q.filter(date__range=(date_min,date_max))


    l = [ ['X' for d in range(0,32)] for m in range(0,12)]
    mnames = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 
              'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    for mon in range(0,12):
        l[mon][0] = mnames[mon]

    for ordday in range(ord_min, ord_max + 1):
        thedate = datetime.date.fromordinal(ordday)
        m = (thedate.month + 5) % 12
        d = thedate.day 
        l[m][d] = ''
        daytours = q.filter(date__exact=thedate)
        dayhours = 0
        for tour in daytours:
            dayhours += tour.tour_length()
        if dayhours > 0:
            l[m][d]  = str(dayhours)

    return render(request, 'personnel/aps11.html', 
                  {"person": person, 
                   "cal": l,
                   "daylabels": ['Mon'] + range(1,32)})

def aps10_html(request, year, month, day):
    date = datetime.date(int(year),int(month),int(day))

    TourFormSet = modelformset_factory(Tour, can_delete=True)
    if request.method == 'POST':
        formset = TourFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('aps10_html', 
                                                kwargs={"year": year,
                                                        "month": month,
                                                        "day": day}))
    else:
        formset = TourFormSet(queryset=Tour.objects.filter(date__exact=date))
    return render_to_response("personnel/aps10.html", 
                              {"date": date,
                               "formset": formset },
                              context_instance=RequestContext(request))

def aps36_html (request, y, m):
    year= int(y)
    month = int(m)
    day = datetime.timedelta(1)
    date_min = datetime.date(year,month,1)
    
    date_max = datetime.date(year + (month/12), 1 + (month % 12),1) - day

    tours = Tour.objects.filter(date__range=(date_min,date_max))
    # FIXME actually, just people in the unit during the month
    people = Person.objects.all()
    
    
    data = []
    for person in people:
        qp = tours.filter(person=person) 
        hours = 0
        for tour in qp:
            hours += tour.tour_length()
        data += [[person, hours]]
    return render(request, 'personnel/aps36.html', 
                  {"data": data,
                   "date": date_min.strftime("%B %Y")})

        
    
