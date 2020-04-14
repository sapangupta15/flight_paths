from unittest.mock import patch

from flight_paths.models.response import Route, Response
from flight_paths.service.flight_path_service import get_paths, get_alternate_path


@patch('flight_paths.service.flight_path_service.get_route_details')
@patch('flight_paths.service.flight_path_service.get_airport')
@patch('flight_paths.service.flight_path_service.get_alternate_path')
@patch('flight_paths.service.flight_path_service.get_shortest_route')
def test_get_paths_returns_shortest_path_only_if_alternate_path_not_available(mock_shortest_path,
                                                                              mock_alternate_path,
                                                                              mock_airports,
                                                                              mock_route_details):
    mock_shortest_path.return_value = [4364, 2975, 2965]
    mock_alternate_path.return_value = None
    mock_airports.side_effect = ['airport1-country1', 'airport2-country2']

    mock_route = Route('airport10', 'airport20', 'airline1', '300.12', '2 hours,10 mins',[[10,20],[25,50]])
    mock_route_details.return_value = mock_route

    expected_response = Response(source='airport1-country1', destination='airport2-country2', routes=[mock_route])
    response = get_paths(source='a', destination='b', max_hops=0)
    assert response == expected_response.to_json()
    mock_shortest_path.assert_called_once()
    mock_alternate_path.assert_called_once()
    assert mock_airports.call_count == 2
    mock_route_details.assert_called_once()


@patch('networkx.nx.all_simple_paths')
def test_get_alternate_pathdoes_not_return_same_route_as_shortest_route(mock_simple_paths):
    """
    mock networkx api to return same path as shortest path
    :param mock_simple_paths:
    :return:
    """
    mock_simple_paths.return_value = [[1, 2]]
    shortest_path = [1, 2]
    alternate_path = get_alternate_path('a', 'b', 0, shortest_path)
    assert alternate_path is None
    mock_simple_paths.asset_called_once()


@patch('networkx.nx.all_simple_paths')
def test_get_alternate_path_does_not_return_path_if_hops_exceeded(mock_simple_paths):
    """
    mock networkx api to return path with more hops than allowed
    :param mock_simple_paths:
    :return:
    """
    hops = 2
    mock_simple_paths.return_value = [[1, 2, 3, 4, 5]]
    shortest_path = [1, 2]
    alternate_path = get_alternate_path('a', 'b', 0, shortest_path)
    assert alternate_path is None
    mock_simple_paths.asset_called_once()
