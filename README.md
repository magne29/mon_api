
# Système Intelligent de Gestion de Tickets (mon_api)

Ce projet est une solution backend robuste développée avec **Django** et **Django REST Framework (DRF)**. Il automatise la gestion du support client en intégrant une intelligence artificielle pour la classification et un algorithme de répartition de charge pour les agents.
##Mode de Fonctionnement de l'API

L'originalité de cette API réside dans son flux de traitement automatisé. Voici ce qui se passe lorsqu'un ticket est créé :
 1. Analyse par Intelligence Artificielle (NLP Mock)
Lorsqu'un utilisateur envoie un ticket via `POST /api/ticket/`, l'API analyse le `subject` et la `description`. 
- **Logique** : Le système scanne des mots-clés (ex: "facture", "paiement", "erreur", "technique").
- **Action** : L'IA détermine automatiquement le **Département** approprié (ex: Département 2 pour la Facturation).
- **Avantage** : Plus besoin de tri manuel, les tickets arrivent directement dans le bon service.
 2. Algorithme de Répartition de Charge (Load Balancing)
Une fois le département identifié, le système ne choisit pas un agent au hasard.
- **Calcul de charge** : Le système compte le nombre de tickets "ouverts" pour chaque agent du département cible.
- **Attribution** : Le ticket est automatiquement assigné à l'agent qui a **le moins de travail** (la charge la plus faible).
- **Résultat** : Une distribution équitable des tâches et une meilleure réactivité du support.
 3. Sécurité et Documentation
- **JWT (JSON Web Tokens)** : Toutes les routes sensibles sont protégées. Un utilisateur doit être authentifié pour interagir avec les tickets.
- **Swagger UI** : Une documentation interactive est disponible, permettant de tester chaque fonctionnalité en temps réel.

##  Installation et Configuration

 1. Installation
```bash
git clone <votre-url-github>
cd ma_sn
uv sync  # ou pip install -r requirements.txt

2. Base de données et Super-utilisateur
Bash
python manage.py migrate
python manage.py createsuperuser

3. Utilisation
Point d'entrée de bienvenue
En accédant à /api/, vous recevrez un message de guidage :
JSON
{
  "message": "Bienvenue sur l'API de Routage de Tickets",
  "documentation": "/api/docs/",
  "endpoints_principaux": "/api/ticket/"
}

4.Accès à la Documentation
Rendez-vous sur http://127.0.0.1:8000/api/docs/ pour :
-Générer un token via le endpoint /api/token/.
-S'authentifier avec le bouton Authorize (format: Bearer <votre_token>).
-Tester la création de tickets.

5.endpointS API
Catégorie,Méthode,URL,Description
Accueil,GET,/api/,Message de bienvenue et liens rapides.
Authentification,POST,/api/token/,Obtenir les jetons Access et Refresh.
Authentification,POST,/api/token/refresh/,Renouveler un jeton Access expiré.
Documentation,GET,/api/docs/,Interface Swagger UI interactive.
Documentation,GET,/api/schema/,Schéma OpenAPI brut (YAML/JSON).
Tickets,GET,/api/ticket/,Liste tous les tickets (nécessite Auth).
Tickets,POST,/api/ticket/,Créer un ticket (Déclenche l'IA et le Routage).
Tickets,GET,/api/ticket/{id}/,Voir les détails d'un ticket spécifique.
Actions,POST,/api/ticket/{id}/reassign/,Réassigner manuellement un ticket.
Agents,GET,/api/agent/,Liste des agents et leur charge actuelle.

5. Technologies Utilisées
-Framework : Django & Django REST Framework
-Authentification : SimpleJWT (JWT)
-Documentation : Drf-spectacular (Swagger UI)
-Langage : Python 3.11+

AUTEUR: MAGNE CORETTA VERLEINE
prjet dev web avec python
