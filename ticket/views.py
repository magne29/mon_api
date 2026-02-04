from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample  # Import manquant

from .models import Ticket, Department, Agent
from .serializers import TicketSerializer, DepartmentSerializer
from .utils import classify_ticket

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class TicketViewSet(viewsets.ModelViewSet):

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @extend_schema(
        summary="Créer un nouveau ticket avec IA",
        description="Analyse le sujet et la description pour assigner automatiquement un département et un agent.",
        examples=[
            OpenApiExample(
                'Exemple de ticket facturation',
                value={
                    "subject": "Problème de paiement",
                    "description": "J'ai été débité deux fois pour mon abonnement.",
                    "priority": "HIGH"
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):

        ticket = serializer.save()


        dep_name, confidence = classify_ticket(ticket.description)
        department = Department.objects.filter(name=dep_name).first()

        if department:
            ticket.assigned_department = department


            agent = Agent.objects.filter(
                department=department,
                is_available=True
            ).order_by('current_workload').first()

            if agent:
                ticket.assigned_agent = agent
                agent.current_workload += 1
                agent.save()

            ticket.save()

    @action(detail=True, methods=['get'], url_path='suggest-department')
    def suggest_department(self, request, pk=None):
        ticket = self.get_object()
        prediction, confidence = classify_ticket(ticket.description)

        return Response({
            'ticket_id': ticket.id,
            'current_description': (ticket.description[:100] + "...") if ticket.description else "",
            'suggested_department': prediction,
            'confidence_score': round(confidence, 2),
            'needs_human_review': confidence < 0.6
        })

    @action(detail=True, methods=['patch'], url_path='reassign')
    def reassign(self, request, pk=None):
        ticket = self.get_object()
        new_department_id = request.data.get('department_id')

        if not new_department_id:
            return Response(
                {"error": "Le champ 'department_id' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            new_dep = Department.objects.get(id=new_department_id)
        except (Department.DoesNotExist, ValueError):
            return Response(
                {"error": "Département introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )


        if ticket.assigned_agent:
            ticket.assigned_agent.current_workload = max(0, ticket.assigned_agent.current_workload - 1)
            ticket.assigned_agent.save()


        ticket.assigned_department = new_dep

        new_agent = Agent.objects.filter(
            department=new_dep,
            is_available=True
        ).order_by('current_workload').first()

        if new_agent:
            ticket.assigned_agent = new_agent
            new_agent.current_workload += 1
            new_agent.save()
            agent_name = new_agent.user.username if hasattr(new_agent.user, 'username') else str(new_agent)
        else:
            ticket.assigned_agent = None
            agent_name = "Aucun agent disponible"

        ticket.save()

        return Response({
            "status": "Réassignation réussie",
            "ticket_id": ticket.id,
            "new_department": new_dep.name,
            "new_agent": agent_name
        })