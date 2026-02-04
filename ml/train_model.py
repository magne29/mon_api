import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import os

# 1. Chargement
csv_path = 'customer_support_tickets.csv'
try:
    df = pd.read_csv(csv_path)

    # 2. Mapping des noms du CSV vers tes départements Django
    # Le CSV contient : 'Technical issue', 'Billing inquiry', 'Product inquiry', 'Refund request'
    category_map = {
        'Technical issue': 'Technique',
        'Billing inquiry': 'Facturation',
        'Refund request': 'Facturation',
        'Product inquiry': 'Commercial',
        'Cancellation request': 'SAV'
    }

    # Appliquer le mapping et supprimer les lignes vides
    df['label'] = df['Ticket Type'].map(category_map).fillna('SAV')
    X = df['Ticket Description']
    y = df['label']

    # 3. Création du Pipeline
    model = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
        ('clf', LinearSVC())
    ])

    print("Entraînement en cours sur le dataset Kaggle...")
    model.fit(X, y)

    # 4. Sauvegarde (Remonte d'un dossier pour être à la racine de mon_api)
    output_path = os.path.join('..', 'ticket_classifier.joblib')
    joblib.dump(model, output_path)

    print(f"Succès ! Modèle sauvegardé ici : {os.path.abspath(output_path)}")

except Exception as e:
    print(f"Erreur : {e}")