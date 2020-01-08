from django.db import models

# Create your models here.
class candidate(models.Model):
    CERTIFICATE_OPTIONS = [
        ('CA', 'Campus Ambassador'),
        ('P' , 'Participant' ),
        ('W' , 'Winner'),
    ]

    EVENT_OPTIONS = [
        ('Dance', 'Electric Heels'),
        ('Music' , 'Raga High' ),
        ('Drama' , 'Street Play'),
    ]
    alcher_id = models.CharField(max_length=255 , null=False)
    name = models.CharField(max_length=255 , null=False)
    certificate_type = models.CharField(max_length=30, choices=CERTIFICATE_OPTIONS, default='CA' , blank = False)
    is_generated = models.BooleanField(default = None)
    is_valid = models.BooleanField(default = None)
    certificate_url = models.CharField(max_length=255 , blank=True)
    event = models.CharField(max_length=30, choices=EVENT_OPTIONS, default='' , blank = False)

    def __str__(self):
        return self.name









