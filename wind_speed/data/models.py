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

    
class GeneralData(models.Model):
    no_states = models.IntegerField('states amount')
    no_departments = models.IntegerField('department amount')
    no_records = models.IntegerField('Records amount')

    class Meta:
        verbose_name = 'general data'

    def __str__(self):
        return self.pk


class LocationData(models.Model):
    location = models.CharField('location', max_length=20)
    name = models.CharField('department', max_length=100)
    avg_speed = models.FloatField('average speed')
    median_speed = models.FloatField('median speed')
    dev_speed = models.FloatField('standard deviation speed')
    min_speed = models.FloatField('minimum speed')
    max_speed = models.FloatField('maximum speed')
    avg_direction = models.FloatField('average direction')
    median_direction = models.FloatField('median direction')
    dev_direction = models.FloatField('standard deviation direction')

    class Meta:
        verbose_name = 'location data'
        verbose_name_plural = 'locations data'
        ordering = ['name']

    def __str__(self):
        return f'{dict(self.LOCATIONS_ENUM)[self.location]} - {self.name}'

    
class LocationMonthData(models.Model):
    location = models.CharField('location', max_length=20)
    name = models.CharField('department', max_length=100)
    month = models.IntegerField('month', validators=[MaxValueValidator(12), MinValueValidator(1)])
    avg_speed = models.FloatField('average speed')
    median_speed = models.FloatField('median speed')
    dev_speed = models.FloatField('standard deviation speed')
    min_speed = models.FloatField('minimum speed')
    max_speed = models.FloatField('maximum speed')
    avg_direction = models.FloatField('average direction')
    median_direction = models.FloatField('median direction')
    dev_direction = models.FloatField('standard deviation direction')

    class Meta:
        verbose_name = 'location month data'
        verbose_name_plural = 'locations month data'
        ordering = ['name', 'month']

    def __str__(self):
        return f'{dict(self.LOCATIONS_ENUM)[self.location]} - {self.name} - {self.month}'