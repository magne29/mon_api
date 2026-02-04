from rest_framework import serializers
from .models import Ticket, Department, Agent

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'priority', 'assigned_department', 'assigned_agent']
        read_only_fields = ['assigned_department', 'assigned_agent']