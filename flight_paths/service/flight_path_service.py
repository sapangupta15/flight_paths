import networkx as nx
from flight_paths.service import route_network
from flight_paths.service.route_details_service import get_airport, get_route_details
from flight_paths.models.response import Response
from flight_paths.exceptions.processing_exception import ProcessingException
from flight_paths.utils.logger import logger


def get_shortest_route(source, destination):
    """
    calculate shortest path between source and destination.
    :param source:
    :param destination:
    :return:
    """
    shortest_route = nx.shortest_path(route_network,
                                      source=source,
                                      target=destination,
                                      weight='Distance')
    return shortest_route


def get_alternate_path(source, destination, max_hops, shortest_route):
    """
    find backup route such that it does not exceed specified number of hops
    and is different from shortest path
    :param source:
    :param destination:
    :param max_hops:
    :param shortest_route:
    :return:
    """
    for cutoff in range(2, max_hops+2):
        all_paths = nx.all_simple_paths(route_network, source=source, target=destination, cutoff=cutoff)
        for path in all_paths:
            if path != shortest_route and len(path) <= max_hops+2:
                return path
    return None


def get_paths(source, destination, max_hops):
    """
    calulcate 2 routes - shortest and a back, not exceeding max_hops
    :param source:
    :param destination:
    :param max_hops:
    :return:
    """
    routes = []
    try:
        shortest_route = get_shortest_route(source, destination)
        if shortest_route:
            routes.append(shortest_route)
        backup_route = get_alternate_path(source, destination, max_hops,
                                          shortest_route=shortest_route)
        if backup_route:
            routes.append(backup_route)
    except nx.exception.NetworkXNoPath as nx_exc:
        logger.exception('No flight paths found')
        raise ProcessingException(f'No route found between source and destination')
    except nx.exception.NodeNotFound as node_miss_exc:
        logger.exception('Node not found in network')
        raise ProcessingException(f'Node is not available, please contact dev team to fix data')
    except Exception as e:
        logger.exception('Unexpected exception raised')
        raise ProcessingException('Unhandled exception has occurred, please contact development/support teams ')

    response = Response(
        source=get_airport(source),
        destination=get_airport(destination),
        routes=[get_route_details(route) for route in routes]
    )
    return response.to_json()
