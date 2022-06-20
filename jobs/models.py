from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

class References(models.Model):
    file = models.FileField(upload_to='references/')

    def __str__(self) -> str:
        return self.file.url


class Jobs(models.Model):
    category_choices = (('D', 'Design'),
                     ('VE', 'Video Edition'))
    
    status_choices = (('AW', 'At working'),
                    ('WA', 'Waiting approval'),
                    ('DE', 'Delivered'))

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=2, choices=category_choices, default='D')
    deadline = models.DateTimeField()
    price = models.FloatField()
    references = models.ManyToManyField(References)
    professional = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    reserved = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=status_choices, default='W')
    work_file = models.FileField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='creator')
    
    def __str__(self) -> str:
        return self.title