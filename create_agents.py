import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ma_sn.settings')
django.setup()

from django.contrib.auth.models import User
from ticket.models import Agent, Department


def setup_agents():
    # 1. On s'assure que les départements existent
    tech_dep = Department.objects.filter(name='Technique').first()

    if not tech_dep:
        print("Erreur : Lance d'abord tes migrations de départements !")
        return

    # 2. Création de 2 agents de test pour le département Technique
    agents_data = [
        {'username': 'agent_alice', 'name': 'Alice Tech'},
        {'username': 'agent_bob', 'name': 'Bob Tech'},
    ]

    for data in agents_data:
        user, created = User.objects.get_or_create(username=data['username'])
        if created:
            user.set_password('password123')
            user.save()

        agent, a_created = Agent.objects.get_or_create(
            user=user,
            defaults={'department': tech_dep, 'is_available': True, 'current_workload': 0}
        )
        print(f"Agent {data['name']} prêt !")


if __name__ == "__main__":
    setup_agents()