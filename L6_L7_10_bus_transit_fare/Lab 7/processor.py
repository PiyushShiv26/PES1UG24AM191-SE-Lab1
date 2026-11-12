import math
import re


def parse_transit_corridor(corridor_code):
    """Parse a corridor code in ORIGIN-DESTINATION-ZONES format."""
    if not isinstance(corridor_code, str):
        return None

    parts = corridor_code.strip().split("-")
    if len(parts) != 3:
        return None

    orig, dest, zones_str = (part.strip() for part in parts)
    if not orig or not dest or not re.fullmatch(r"[A-Za-z0-9]+", orig) or not re.fullmatch(r"[A-Za-z0-9]+", dest):
        return None
    if not re.fullmatch(r"[0-9]+", zones_str):
        return None

    try:
        zones = int(zones_str)
    except (ValueError, OverflowError):
        return None
    if zones <= 0:
        return None

    base_fare = 2.50 + (zones * 0.75)
    return f"Route {orig.upper()}->{dest.upper()}: {zones} Zones, Fare ${base_fare:.2f}"


def lookup_concession_discount(category_name):
    """Return the fare multiplier for a supported concession category."""
    if not isinstance(category_name, str):
        return None

    category = category_name.strip().upper()
    discounts = {
        "STANDARD": 1.00,
        "STUDENT": 0.50,
        "SENIOR": 0.35,
        "MILITARY": 0.20,
        "CHILD": 0.00,
    }
    if category not in discounts:
        return None
    return discounts[category]


def compute_passenger_density(occupancy_ratio_str):
    """Compute passengers per kilometre from a 'passengers/km' string."""
    if not isinstance(occupancy_ratio_str, str):
        return None

    parts = occupancy_ratio_str.strip().split("/")
    if len(parts) != 2 or not all(part.strip() for part in parts):
        return None

    try:
        passengers = float(parts[0].strip())
        km = float(parts[1].strip())
    except (ValueError, TypeError):
        return None

    if not math.isfinite(passengers) or not math.isfinite(km):
        return None
    if passengers < 0:
        return None
    if km <= 0:
        return None

    density = passengers / km
    if not math.isfinite(density):
        return None
    return round(density, 2)


def main():
    print("==== Running parse_transit_corridor ====")
    c_input = input("Enter corridor (e.g. DT-UP-3): ")
    result = parse_transit_corridor(c_input)
    print(result if result is not None else "Invalid corridor input.")

    print("\n==== Running lookup_concession_discount ====")
    cat_input = input("Enter concession category (e.g. STUDENT, SENIOR): ")
    result = lookup_concession_discount(cat_input)
    print("Multiplier:", result) if result is not None else print("Invalid concession category.")

    print("\n==== Running compute_passenger_density ====")
    d_input = input("Enter passengers/km (e.g. 50/10.0): ")
    result = compute_passenger_density(d_input)
    print("Density:", result) if result is not None else print("Invalid occupancy ratio.")


if __name__ == "__main__":
    main()
