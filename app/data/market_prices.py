from app.models.agriculture import MarketPrice
from datetime import datetime

# Prix simulés (FCFA) - Dernière mise à jour simulée
def get_current_prices():
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        MarketPrice(crop_name="Cacao", price_avg_fcfa=1500.0, unit="kg", trend="monte", last_updated=today),
        MarketPrice(crop_name="Café Robusta", price_avg_fcfa=1100.0, unit="kg", trend="stable", last_updated=today),
        MarketPrice(crop_name="Café Arabica", price_avg_fcfa=2300.0, unit="kg", trend="monte", last_updated=today),
        MarketPrice(crop_name="Maïs", price_avg_fcfa=250.0, unit="kg", trend="stable", last_updated=today),
        MarketPrice(crop_name="Riz", price_avg_fcfa=450.0, unit="kg", trend="monte", last_updated=today),
        MarketPrice(crop_name="Tomate", price_avg_fcfa=800.0, unit="panier", trend="baisse", last_updated=today), # Panier standard
        MarketPrice(crop_name="Plantain", price_avg_fcfa=3500.0, unit="régime", trend="stable", last_updated=today),
        MarketPrice(crop_name="Pomme de terre", price_avg_fcfa=400.0, unit="kg", trend="stable", last_updated=today),
        MarketPrice(crop_name="Oignon", price_avg_fcfa=600.0, unit="kg", trend="monte", last_updated=today),
        MarketPrice(crop_name="Huile de palme", price_avg_fcfa=900.0, unit="litre", trend="stable", last_updated=today),
    ]

def get_price_by_crop(crop_name: str):
    prices = get_current_prices()
    for price in prices:
        if crop_name.lower() in price.crop_name.lower():
            return price
    return None
