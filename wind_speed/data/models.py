from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class HourSpeed(models.Model):
    hour = models.IntegerField('date')
    avgSpeed = models.FloatField('average speed')
    medSpeed = models.FloatField('median speed')

    class Meta:
        verbose_name = 'hour speed'
        verbose_name_plural = 'hours speed'
        ordering = ['hour']

    def __str__(self):
        return f'Wind speed in {self.hour}'

    
class GeneralData(models.Model):
    noStates = models.IntegerField('states amount')
    noDepartments = models.IntegerField('department amount')
    noRegions = models.IntegerField('regions amount')
    noStations = models.IntegerField('stations amount')
    noRecords = models.IntegerField('records amount')

    class Meta:
        verbose_name = 'general data'

    def __str__(self):
        return 'General data'


class LocationData(models.Model):
    location = models.CharField('location', max_length=20)
    name = models.CharField('name', max_length=100)
    avgSpeed = models.FloatField('average speed')
    medianSpeed = models.FloatField('median speed')
    devSpeed = models.FloatField('standard deviation speed')
    minSpeed = models.FloatField('minimum speed')
    maxSpeed = models.FloatField('maximum speed')
    avgDirection = models.FloatField('average direction')
    medianDirection = models.FloatField('median direction')
    devDirection = models.FloatField('standard deviation direction')

    class Meta:
        verbose_name = 'location data'
        verbose_name_plural = 'locations data'
        ordering = ['name']

    def __str__(self):
        return f'{self.location} - {self.name}'

    
class LocationMonthData(models.Model):
    location = models.CharField('location', max_length=20)
    name = models.CharField('name', max_length=100)
    month = models.IntegerField('month', validators=[MaxValueValidator(12), MinValueValidator(1)])
    avgSpeed = models.FloatField('average speed')
    medianSpeed = models.FloatField('median speed')
    devSpeed = models.FloatField('standard deviation speed')
    minSpeed = models.FloatField('minimum speed')
    maxSpeed = models.FloatField('maximum speed')
    avgDirection = models.FloatField('average direction')
    medianDirection = models.FloatField('median direction')
    devDirection = models.FloatField('standard deviation direction')

    class Meta:
        verbose_name = 'location month data'
        verbose_name_plural = 'locations month data'
        ordering = ['name', 'month']

    def __str__(self):
        return f'{self.location} - {self.name} - {self.month}'


class GeoData(models.Model):
    location = models.CharField('location', max_length=20)
    name = models.CharField('name', max_length=100)
    area = models.FloatField('area', null=True)
    perimeter = models.FloatField('perimeter', null=True)
    hectares = models.FloatField('hectares', null=True)
    geometry = models.JSONField('geometry')

    class Meta:
        verbose_name = 'location geometry data'
        verbose_name_plural = 'locations geometry data'
        ordering = ['name']

    def __str__(self):
        return f'{self.location} - {self.name}'