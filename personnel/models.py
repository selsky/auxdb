from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Min

# Create your models here.

RANK_CHOICES = (
    ('Civilian', 
     (('APP', 'Applicant'),
      ('BTC', 'Enrolled in BTC'),
      ('QUAL', 'Approved and Qualified'))),
    ('Auxiliary',
     (('APO',    'Auxiliary Police Officer'),
      ('A/Sgt',  'Auxiliary Sergeant'),
      ('A/Lt',   'Auxiliary Lieutenant'),
      ('A/Capt', 'Auxiliary Captain'),
      ('A/DI',   'Auxiliary Deputy Inspector'),
      ('A/Insp', 'Auxiliary Inspector'),
      ('A/DC',   'Auxiliary Deputy Chief'))))

def fake_idno():
    try:
        n = Person.objects.aggregate(Min('idno'))['idno__min']
    except:
        n = 0
    if n == None:
        n = 0
    if n > 0:
        n = 0
    return n-1

def valid_idno(no):
    if (no > 0 and no < 300000):
        raise ValidationError('%s too small' % no)
    if (no > 999999):
        raise ValidationError('%s too large' % no)
    if (no < -10000):
        raise ValidationError('%s too negative' % no)

class Person(models.Model):
    last_name = models.CharField(max_length = 40)
    first_name = models.CharField(max_length = 40)
    rank = models.CharField(max_length = 7, choices = RANK_CHOICES)
    idno = models.SmallIntegerField(unique = True, 
                                    primary_key = True, 
                                    validators = [valid_idno],
                                    default=fake_idno)
    shield = models.SmallIntegerField(null = True,
                                      blank = True)
