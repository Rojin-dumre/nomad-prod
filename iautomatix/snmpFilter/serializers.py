from rest_framework import serializers
from .models import Information, Snmp

class SnmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snmp
        fields ='__all__'