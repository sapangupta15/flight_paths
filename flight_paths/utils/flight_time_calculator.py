def calculate_flight_time(distance):
    """
    The logic to calcuate time has been borrowed from OpenFLights FAQ:
    https://openflights.org/faq
    30 min plus 1 hour per every 500 miles
    :param distance:
    :return:
    """
    distance_in_miles = distance/1.609
    time_in_mins = (distance_in_miles/500) * 60 + 30
    number_of_hours = int(time_in_mins // 60)
    number_of_minutes = int(time_in_mins % 60)
    estimated_time = f'{str(number_of_hours)} hours {str(number_of_minutes)} minutes'
    return estimated_time
