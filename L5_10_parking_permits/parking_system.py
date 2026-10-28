"""Parking permit registration and zone monitoring."""

import json
import random
from datetime import datetime, timedelta

# Global state
permits = {}
ZONES = ["A", "B", "C"]


def register_permit(vehicle_plate, zone_id, zone_records=None):
    """Register a permit if the plate and zone are valid."""
    if not isinstance(vehicle_plate, str) or not vehicle_plate.strip():
        return None

    if zone_id not in ZONES:
        return None

    if zone_records is None:
        zone_records = []

    permit_no = "P" + str(random.randint(10000, 99999))
    expiry = datetime.now() + timedelta(days=180)

    permits[vehicle_plate] = {
        "zone": zone_id,
        "permit": permit_no,
        "expiry": expiry.strftime("%Y-%m-%d"),
    }
    zone_records.append((vehicle_plate, zone_id))

    return permit_no


def revoke_permit(vehicle_plate):
    """Revoke a permit if one exists for the supplied plate."""
    return permits.pop(vehicle_plate, None) is not None


def is_expired(vehicle_plate):
    """Return whether a registered permit has expired."""
    permit = permits.get(vehicle_plate)

    if permit is None:
        return False

    try:
        expiry = datetime.strptime(permit["expiry"], "%Y-%m-%d")
    except (KeyError, TypeError, ValueError):
        return False

    return expiry < datetime.now()


def scan_zone(zone_id, plates_seen):
    """Return plates that are unregistered, misplaced, or expired."""
    flagged = []

    for plate in plates_seen:
        permit = permits.get(plate)

        if (
            permit is None
            or permit["zone"] != zone_id
            or is_expired(plate)
        ):
            flagged.append(plate)

    return flagged


def load_permit_database(file="permits.json"):
    """Load permits from JSON, returning an empty database if unavailable."""
    try:
        with open(file, "r", encoding="utf-8") as database_file:
            loaded_permits = json.load(database_file)
    except (OSError, json.JSONDecodeError):
        return {}

    if isinstance(loaded_permits, dict):
        return loaded_permits

    return {}


def save_permit_database(file="permits.json"):
    """Save the current permits to a JSON file."""
    with open(file, "w", encoding="utf-8") as database_file:
        json.dump(permits, database_file, indent=2)


def set_expiry(vehicle_plate, date_text):
    """Update a permit's expiry date when the date is valid."""
    permit = permits.get(vehicle_plate)

    if permit is None:
        return False

    try:
        expiry = datetime.strptime(date_text, "%Y-%m-%d")
    except (TypeError, ValueError):
        return False

    permit["expiry"] = expiry.strftime("%Y-%m-%d")
    return True


def main():
    """Run the parking permit management workflow."""
    permits.clear()
    permits.update(load_permit_database())
    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")
    register_permit("", "B")
    register_permit(None, "C")
    set_expiry("KA01AB1234", "2020-01-01")
    revoke_permit("MH12ZZ0000")
    print("Flagged in zone A:", scan_zone(
        "A", ["KA01AB1234", "KA05XY9999", "TN09QQ1111"]))
    plate = input("Plate to revoke (Enter to skip): ")
    revoke_permit(plate)
    save_permit_database()
    print("Permits on file:", len(permits))


if __name__ == "__main__":
    main()
