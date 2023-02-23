from django.db import models

# Create your models here.


class Information(models.Model):
    host = models.CharField(max_length=200, null=True, blank=False, unique=True)
    hostname = models.CharField(max_length=200, null=True, blank=False)
    port = models.IntegerField()
    platform = models.CharField(max_length=200, null=True, blank=False)
    username = models.CharField(max_length=200, null=True, blank=False)
    password = models.CharField(max_length=200, null=True, blank=False)
    groups = models.CharField(max_length=200, null=True, blank=False)

    def __str__ (self):
        return self.host

class Snmp(models.Model):
    host_snmp = models.ForeignKey(Information, on_delete=models.CASCADE, to_field='host')
    community = models.CharField(max_length=200, null=True, blank=False)

    