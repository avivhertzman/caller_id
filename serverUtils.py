#!flask/bin/python
import re

from flask import Flask, jsonify, abort, request, make_response, url_for
from csv_fetcher import init_data, get_by_phone_number, delete_by_phone_number
from flask_parameter_validation import ValidateParameters, Query
from typing import Optional


app = Flask(__name__, static_url_path="")


# reop = dataRepo(get_data)

@app.before_first_request
def _run_on_start():
    init_data()


@app.errorhandler(400)
def bad_request(error):
    if error.description:
        return make_response(jsonify({'error': error.description}), 400)
    return make_response(jsonify({'error': "Bad request"}), 400)


@app.errorhandler(500)
def internal_server_eror(error):
    if error.description:
        return make_response(jsonify({'error': error.description}), 500)
    return make_response(jsonify({'error': "not found"}), 500)


@app.errorhandler(404)
def not_found(error):
    if error.description:
        return make_response(jsonify({'error': error.description}), 404)
    return make_response(jsonify({'error': "not found"}), 404)


@app.route('/caller_id', methods=['GET'])
def get_person_phone_number():
    number = (request.args.get('phone_number'))
    validate_input(number)
    result = get_by_phone_number(number)
    if len(result) == 0:
        abort(404, "phone number does not exist")
    return result

@app.route('/remove', methods=['POST'])
def remove_phone_number():
    number = (request.args.get('phone_number'))
    validate_input(number)
    delete_by_phone_number(number)
    return make_response({}, 202)
def validate_input(number):
    if number is None or re.fullmatch('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', number) is None:
        abort(400, 'number provided was not in phone number format')



if __name__ == '__main__':
    app.run(debug=True)
