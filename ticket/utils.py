import joblib
import os
from django.conf import settings

#
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ticket_classifier.joblib')


def classify_ticket(description):



    if not os.path.exists(MODEL_PATH):

        return "SAV", 0.0

    try:
        model = joblib.load(MODEL_PATH)
        prediction = model.predict([description])[0]
        return prediction, 0.85
    except Exception as e:
        print(f"Erreur lors de la classification : {e}")
        return "SAV", 0.0