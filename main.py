from datetime import datetime
import requests

BASE_URL = "https://metrofueltracker.com/api/stations"
HEADERS = {"x-mf-client": "bayanihan-v1"}

QUERY_AREA = {
    "south": 14.5458,
    "west": 120.7867,
    "north": 14.6445,
    "east": 121.0312,
}

FUEL_TYPES = {
    "UNLEADED_91": "Unleaded 91",
    "PREMIUM_95": "Premium 95",
    "PREMIUM_98": "Premium 98",
    "DIESEL": "Diesel",
    "PREMIUM_DIESEL": "Premium Diesel",
}

DISPLAY_ORDER = [
    "UNLEADED_91",
    "PREMIUM_95",
    "PREMIUM_98",
    "DIESEL",
    "PREMIUM_DIESEL",
]

def build_post_text() -> str:
    highest_prices = {}

    for fuel_code, fuel_label in FUEL_TYPES.items():
        params = {"fuelType": fuel_code, **QUERY_AREA}

        response = requests.get(
            BASE_URL,
            headers=HEADERS,
            params=params,
            timeout=20,
        )
        response.raise_for_status()

        data = response.json()
        stations = data.get("stations", [])

        highest_price = None

        for station in stations:
            prices = station.get("prices", {})
            fuel_info = prices.get(fuel_code)

            if not fuel_info:
                continue

            price = fuel_info.get("price")
            if price is None:
                continue

            if highest_price is None or price > highest_price:
                highest_price = price

        if highest_price is not None:
            highest_prices[fuel_code] = {
                "label": fuel_label,
                "price": highest_price,
            }

    now = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    lines = [
        "FUEL PRICE ADVISORY PH",
        "",
        f"As of {now}",
        "",
        "Fuel prices can go up as much as:",
        "",
    ]

    for fuel_code in DISPLAY_ORDER:
        info = highest_prices.get(fuel_code)
        if info:
            lines.append(f"{info['label']}: PHP {info['price']:.2f}")

    if len(lines) == 6:
        lines.append("As of this check, there are no fresh monitored prices yet.")

    lines += [
        "",
        "Based on monitored station prices.",
        "Prices may vary by location.",
    ]

    return "\n".join(lines)

if __name__ == "__main__":
    print(build_post_text())