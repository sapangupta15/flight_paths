from flight_paths.utils.flight_time_calculator import calculate_flight_time, get_distance_in_miles, get_time_in_minutes


def test_get_distance_in_miles_converts_kms_to_miles():
    distance_in_km = 1.609
    assert get_distance_in_miles(distance_in_km) == 1


def test_get_time_in_minutes_returns_estimated_time_in_minutes():
    distance_in_miles = 500
    assert get_time_in_minutes(distance_in_miles) == 90


def test_calculate_flight_time_returns_time_in_hours_and_minutes():
    distance = 804.5
    assert calculate_flight_time(distance) == '1 hours 30 minutes'
