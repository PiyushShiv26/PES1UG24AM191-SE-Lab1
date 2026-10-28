
import pytest

from bus_transit_fare import (
    process_commute_manifest,
    inspect_smartcard_turnstiles,
)


def test_invalid_manifest_input():
    with pytest.raises(ValueError):
        process_commute_manifest("invalid", 2.0)


def test_negative_booking_fee():
    with pytest.raises(ValueError):
        process_commute_manifest([], -1.0)


def test_inactive_route_is_skipped():
    result = process_commute_manifest(
        [{"route_active": False, "route_type": "local"}], 2.0
    )
    assert result == {
        "total_fare": 0.0,
        "status": "ZERO_RIDERSHIP",
    }


@pytest.mark.parametrize(
    ("route_type", "expected_fare"),
    [
        ("express", 7.0),
        ("shuttle", 5.0),
        ("local", 3.5),
    ],
)
def test_route_fares(route_type, expected_fare):
    manifests = [{
        "route_active": True,
        "route_type": route_type,
        "commuters": [{"zones": 1, "type": "regular"}],
    }]
    result = process_commute_manifest(manifests, 2.0)
    assert result["total_fare"] == expected_fare
    assert result["status"] == "COMPLETED"


def test_unknown_route_is_rejected():
    result = process_commute_manifest(
        [{"route_active": True, "route_type": "unknown"}], 2.0
    )
    assert result["status"] == "ZERO_RIDERSHIP"


def test_student_senior_and_regular_fares():
    manifests = [{
        "route_active": True,
        "route_type": "local",
        "commuters": [
            {"zones": 2, "type": "student"},
            {"zones": 2, "type": "senior"},
            {"zones": 2, "type": "regular"},
        ],
    }]
    result = process_commute_manifest(manifests, 2.0)
    assert result["total_fare"] == 8.7
    assert result["status"] == "COMPLETED"


def test_invalid_zones_are_rejected():
    result = process_commute_manifest(
        [{
            "route_active": True,
            "route_type": "local",
            "commuters": [{"zones": 0}],
        }],
        2.0,
    )
    assert result["status"] == "ZERO_RIDERSHIP"


def test_blacklisted_local_passenger():
    result = process_commute_manifest(
        [{
            "route_active": True,
            "route_type": "local",
            "commuters": [
                {"zones": 1, "blacklisted": True},
                {"zones": 1, "type": "regular"},
            ],
        }],
        2.0,
    )
    assert result["total_fare"] == 3.5


def test_blacklisted_express_passenger():
    result = process_commute_manifest(
        [{
            "route_active": True,
            "route_type": "express",
            "commuters": [
                {"zones": 1, "type": "regular"},
                {"zones": 1, "blacklisted": True},
                {"zones": 1, "type": "regular"},
            ],
        }],
        2.0,
    )
    assert result["total_fare"] == 0.0
    assert result["status"] == "ZERO_RIDERSHIP"


def test_priority_boarding_fee():
    result = process_commute_manifest(
        [{
            "route_active": True,
            "route_type": "local",
            "priority_boarding": True,
            "commuters": [{"zones": 1, "type": "regular"}],
        }],
        2.0,
    )
    assert result["total_fare"] == 5.5


def test_audit_rejected_after_five_rejections():
    manifests = [
        {"route_active": True, "route_type": "unknown"}
        for _ in range(5)
    ]
    result = process_commute_manifest(manifests, 2.0)
    assert result == {
        "total_fare": 0.0,
        "status": "AUDIT_REJECTED",
    }


def test_empty_turnstile_data():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"


def test_turnstile_jam():
    assert inspect_smartcard_turnstiles([[4, 5]]) == "TURNSTILE_JAM"


def test_turnstile_operational():
    assert inspect_smartcard_turnstiles([[4, 2, 5]]) == "OPERATIONAL"
