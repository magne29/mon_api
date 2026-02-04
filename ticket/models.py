from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='agents')
    is_available = models.BooleanField(default=True)
    current_workload = models.IntegerField(default=0)  # Nombre de tickets actifs

    def __str__(self):
        return self.user.username


class Ticket(models.Model):
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]

    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    created_at = models.DateTimeField(auto_now_add=True)

    # Relations
    assigned_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)


class RoutingDecision(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    predicted_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    confidence_score = models.FloatField()
    is_corrected_manually = models.BooleanField(default=False)