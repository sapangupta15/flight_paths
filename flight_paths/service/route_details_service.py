from flight_paths.service import data_df, airports_by_id
from flight_paths.models.response import Route
from flight_paths.utils.flight_time_calculator import calculate_flight_time


def get_route_details(route):
    """
    Map all components of a route into Route Object from dataframe row using mapper
    :param route:
    :return:
    """
    route_components = []
    for i in range(len(route) - 1):
        source_airport_id = route[i]
        destination_airport_id = route[i+1]
        data_row = data_df[(data_df['Source_airport_ID'] == source_airport_id) &
                           (data_df['Destination_airport_ID'] == destination_airport_id)].iloc[0]
        route_components.append(map_data_row_to_route(data_row))
    return route_components


def map_data_row_to_route(data_row):
    start_airport = data_row['Source_airport_ID']
    end_airport = data_row['Destination_airport_ID']
    return Route(
        source_airport=get_airport(start_airport),
        destination_airport=get_airport(end_airport),
        airline=data_row['Airline_Name'],
        distance="{:.2f}".format(data_row['Distance']),
        est_travel_time=calculate_flight_time(data_row['Distance']),
        path=[
            [data_row['Source_Longitude'], data_row['Source_Latitude']],
            [data_row['Destination_Longitude'], data_row['Destination_Latitude']]
        ]
    )


def get_airport(airport_id):
    """
    Get airport name and country for a given airport id from airport_by_id_dict
    :param airport_id:
    :return:
    """
    airport = airports_by_id.get(str(airport_id))
    if airport:
        return airport['Name'] + ' - ' + airport['Country']
    else:
        return ''
