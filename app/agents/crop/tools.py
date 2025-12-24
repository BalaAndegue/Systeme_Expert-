# Outils spécifiques pour les cultures
from app.data.planting_calendar import get_planting_info

def check_planting_window(region, crop):
    return get_planting_info(region, crop)
