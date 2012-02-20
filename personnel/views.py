# Create your views here.
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from auxdb.personnel.models import Person

def side_draw(p,x,y,s):
    p.saveState()
    p.translate(x,y)
    p.rotate(-90)
    p.drawString(0,0,s)
    p.restoreState()


def aps1_pdf(request, pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
#    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    person = Person.objects.get(pk=pk)

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    p.drawImage('APS1-Front.tif', 0, 54, 72*8.5, 72*11)

#    p.setFont('Helvetica', 8)
#    p.setLineWidth(0.5)
#    p.setStrokeGray(0.5)
#
#
#    for n in range(1,44):
#        p.line(0, 18*n, 72*8.5, 18*n)
#        p.drawString(18, 18*n + 2, str(18*n))
#
#    for n in range(1,34):
#        p.line(18*n, 0, 18*n, 72*11)
#        p.drawString(18*n + 2, 72*11, str(18*n))
#

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    p.drawString(54,729,person.last_name)
    p.drawString(210,729,person.first_name)

    side_draw(p,582,612,person.last_name)
    side_draw(p,582,477,person.first_name)
    side_draw(p,582,324,str(person.idno))
    side_draw(p,582,171,'024')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


