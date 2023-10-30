from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Wind(models.Model):
    date = models.DateTimeField('date')
    hour = models.IntegerField('hour', validators=[MaxValueValidator(23), MinValueValidator(0)])
    minute = models.IntegerField('minute', validators=[MaxValueValidator(59), MinValueValidator(0)])
    speed = models.FloatField('speed')
    direction = models.IntegerField('angle', validators=[MaxValueValidator(360), MinValueValidator(0)])
    department = models.CharField('department', max_length=100)
    state = models.CharField('state', max_length=100)
    region = models.CharField('region', max_length=100)
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')

    class Meta:
        verbose_name = 'wind'
        verbose_name_plural = 'winds'
        ordering = ['date']

    def __str__(self):
        return f'Wind in {self.date}'