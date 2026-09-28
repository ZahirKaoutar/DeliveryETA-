from pathlib import Path
import joblib
import pandas as pd

# ============================================================
# 1. Configuration des chemins d'accès
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "delivery_eta_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"

# ============================================================
# 2. Chargement du modèle et du preprocessor
# ============================================================
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

print("Modèle et Preprocessor chargés avec succès.")

# ============================================================
# 3. Nouvelle donnée de livraison
# Noms des colonnes alignés sur le dataset d'entraînement
# ============================================================
new_delivery = pd.DataFrame(
    {
        "distance_km": [5.2],
        "prep_time_min": [12.0],
        "multiple_deliveries": [1.0],
        "Delivery_person_Age": [28.0],
        "Delivery_person_Ratings": [4.8],
        "Road_traffic_density": ["Jam"],      # Ex: Jam, High, Medium, Low
        "Type_of_vehicle": ["motorcycle"],     # Ex: motorcycle, scooter, electric_scooter
        "Weatherconditions": ["Sunny"],        # Ex: Sunny, Stormy, Sandstorms, Windstorm, Fog
        "City": ["Urban"],                    # Ex: Urban, Semi-Urban, Metropolitian
        "Festival": ["No"],                    # Ex: No, Yes
    }
)

# ============================================================
# 4. Prétraitement avec le preprocessor sauvegardé
# ============================================================
new_delivery_encoded = preprocessor.transform(new_delivery)

# ============================================================
# 5. Prédiction
# ============================================================
prediction = model.predict(new_delivery_encoded)

print(f"Temps de livraison prédit : {prediction[0]:.2f} minutes")