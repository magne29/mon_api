from django.contrib import admin
from .models import Department, Agent, Ticket



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'is_available')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'priority', 'assigned_department', 'assigned_agent', 'created_at')


from django.contrib import admin

# Register your models here.
