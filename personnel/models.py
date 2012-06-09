from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Min, CharField, SmallIntegerField, DateField, BooleanField
from django.contrib.localflavor.us.models import USStateField,USPostalCodeField,PhoneNumberField
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

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

MARITAL_CHOICES = (('M', 'Married'), 
                   ('S', 'Single'),
                   ('D', 'Divorced'),
                   ('W', 'Widowed'))

HAIR_CHOICES = (('Blk', 'Black'), 
                ('Brn', 'Brown'),
                ('Yel', 'Yellow'),
                ('Gry', 'Grey'))

EYE_CHOICES = (('Gy', 'Grey'),
               ('Blu', 'Blue'), 
               ('Hzl', 'Hazel'), 
               ('Br', 'Brown'),
               ('Yel', 'Yellow'),
               ('Gn', 'Green'))

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
    last_name    = CharField(max_length = 40)
    first_name   = CharField(max_length = 40)
    rank         = CharField(max_length = 7, choices = RANK_CHOICES)
    idno         = SmallIntegerField(unique = True, 
                                     primary_key = True, 
                                     validators = [valid_idno],
                                     default=fake_idno)
    shield       = SmallIntegerField(null = True,
                                     blank = True)
    address      = CharField(max_length = 80)
    apt          = CharField(max_length = 8)
    city         = CharField(max_length = 40)
    state        = USStateField()
    zipcode      = CharField(max_length = 10)
    verified     = CharField(max_length = 40)
    phone        = PhoneNumberField()
    birthplace   = CharField(max_length = 80)
    birth_cert   = CharField(max_length = 40)
    voter_no     = CharField(max_length = 40)
    entry_port   = CharField(max_length = 40)
    naturalize   = CharField(max_length = 40)
    green_card   = CharField(max_length = 40)
    other_proof  = CharField(max_length = 40)
    warrant_date = DateField()
    dmv_date     = DateField()
    gender       = CharField(max_length = 2, choices = GENDER_CHOICES)
    marital      = CharField(max_length = 2, choices = MARITAL_CHOICES)
    height       = CharField(max_length = 6)
    weight       = SmallIntegerField()
    hair_color   = CharField(max_length = 4, choices = HAIR_CHOICES)
    eye_color    = CharField(max_length = 4, choices = EYE_CHOICES)
    aka          = CharField(max_length = 80)
    addicted     = BooleanField()
    mental       = BooleanField()
    marks        = CharField(max_length = 80)
    defects      = CharField(max_length = 80)
    ssn          = CharField(max_length = 12)
    drivers      = CharField(max_length = 80)
    pistol       = CharField(max_length = 80)
    pistol_type  = CharField(max_length = 80)
    draft_status = CharField(max_length = 80)
    discharge    = CharField(max_length = 80)
    branch       = CharField(max_length = 80)
    applied      = BooleanField()
    summonsed    = BooleanField()
    max_grade    = CharField(max_length = 40)
    school       = CharField(max_length = 40)
    location     = CharField(max_length = 40)
    emploer      = CharField(max_length = 80)
    emp_address  = CharField(max_length = 80)
    occupation   = CharField(max_length = 80)
    emp_phone    = PhoneNumberField()
    emp_length   = CharField(max_length = 40)
    next_kin     = CharField(max_length = 80)
    kin_relate   = CharField(max_length = 80)
    kin_addr     = CharField(max_length = 80)
    kin_phone    = PhoneNumberField()
