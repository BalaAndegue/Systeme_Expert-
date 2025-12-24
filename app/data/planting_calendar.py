# Calendrier de plantation simplifié pour le Cameroun
# Format: { Region: { Culture: { 'start': Mois_Debut, 'end': Mois_Fin, 'notes': ... } } }

PLANTING_CALENDAR = {
    "Centre": {
        "Cacao": {"start": "Mars", "end": "Juin", "notes": "Petite campagne de Mars à Juin. Grande campagne en Août."},
        "Maïs": {"start": "Mars", "end": "Avril", "notes": "Première campagne (Mars-Juin). Deuxième campagne (Août-Novembre)."},
        "Arachide": {"start": "Mars", "end": "Avril", "notes": "Semis en début de saison des pluies."},
        "Manioc": {"start": "Mars", "end": "Novembre", "notes": "Peut être planté presque toute l'année, préférence début saison pluies."}
    },
    "Littoral": {
        "Banane": {"start": "Janvier", "end": "Décembre", "notes": "Toute l'année si irrigation, sinon début pluies."},
        "Macabo": {"start": "Mars", "end": "Avril", "notes": "Début de la grande saison des pluies."},
    },
    "Ouest": {
        "Haricot": {"start": "Mars", "end": "Avril", "notes": "Première campagne."},
        "Pomme de terre": {"start": "Mars", "end": "Avril", "notes": "Demande beaucoup d'eau mais pas d'excès."},
        "Maïs": {"start": "Février", "end": "Mars", "notes": "Semis précoce possible."}
    },
    "Nord": {
        "Coton": {"start": "Mai", "end": "Juin", "notes": "Début strict de la saison des pluies."},
        "Sorgho": {"start": "Mai", "end": "Juin", "notes": "Après les premières pluies utiles."},
        "Arachide": {"start": "Mai", "end": "Juin", "notes": "Cycle court recommandé."}
    },
    # ... autres régions par défaut génériques
    "default": {
        "Tomate": {"start": "Septembre", "end": "Octobre", "notes": "Contre-saison souvent préférée pour éviter trop de maladies."},
        "Piment": {"start": "Mars", "end": "Mai", "notes": ""}
    }
}

def get_planting_info(region_name, crop_name):
    region_data = PLANTING_CALENDAR.get(region_name, {})
    if not region_data:
        # Fallback to default or similar region if needed, for strictness return None or generic
        pass
    
    crop_info = region_data.get(crop_name)
    if not crop_info:
        # Check default
        crop_info = PLANTING_CALENDAR["default"].get(crop_name)
    
    return crop_info
