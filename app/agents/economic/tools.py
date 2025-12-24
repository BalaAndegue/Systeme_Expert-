from app.data.market_prices import get_current_prices

def fetch_market_prices():
    return get_current_prices()

def format_prices_for_prompt(prices):
    return "\n".join([f"- {p.crop_name}: {p.price_avg_fcfa} FCFA/{p.unit} ({p.trend})" for p in prices])
