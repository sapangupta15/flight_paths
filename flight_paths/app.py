from flask import Flask, request, make_response
from flask_cors import CORS

from flight_paths.exceptions.input_exception import InvalidInputException
from flight_paths.exceptions.processing_exception import ProcessingException
from flight_paths.service.flight_path_service import get_paths

app = Flask(__name__)
CORS(app)


@app.errorhandler(InvalidInputException)
def handle_bad_request(e):
    return e.message, 400


@app.errorhandler(ProcessingException)
def handle_uncaught_errors(e):
    return e.message, 500


@app.route('/paths', methods=['GET'])
def get_flight_paths():
    """
    This endpoint takes source airport id, destination airport id and max number of halts for backup route
    :return:
    """
    source_airport_id = int(request.args.get('source'))
    destination_airport_id = int(request.args.get('destination'))
    max_halts = int(request.args.get('halts'))
    if source_airport_id is None or destination_airport_id is None or max_halts is None:
        raise InvalidInputException('One or more mandatory request attributes: source/destination/halts missing')
    response = get_paths(source_airport_id, destination_airport_id, max_halts)
    return make_response(response, 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
