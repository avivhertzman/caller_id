#!flask/bin/python
import re
from flask import Flask, jsonify, abort, request, make_response, url_for
from constant import PHONE_NUMBER_REGEX
from data_manager import init_data, get_by_phone_number, delete_by_phone_number
from data_repo import dataRepo

app = Flask(__name__, static_url_path="")

repo = dataRepo(init_data())


@app.errorhandler(400)
def bad_request(error):
    if error.description:
        return make_response(jsonify({'error': error.description}), 400)
    return make_response(jsonify({'error': "Bad request"}), 400)


@app.errorhandler(500)
def internal_server_eror(error):
    if error.description:
        return make_response(jsonify({'error': error.description}), 500)
    return make_response(jsonify({'error': "Internal server error"}), 500)


@app.errorhandler(404)
def not_found(error):
    if error.description:
        return make_response(jsonify({'error': error.description}), 404)
    return make_response(jsonify({'error': "Not found"}), 404)


@app.route('/caller_id', methods=['GET'])
def get_person_phone_number():
    number = (request.args.get('phone_number'))
    validate_input(number)
    result = get_by_phone_number(number, repo)
    if len(result) == 0:
        abort(404, "phone number does not exist")
    return result


@app.route('/remove', methods=['POST'])
def remove_phone_number():
    number = (request.args.get('phone_number'))
    validate_input(number)
    delete_by_phone_number(number, repo)
    return make_response({}, 202)


def validate_input(number):
    if number is None or re.fullmatch(PHONE_NUMBER_REGEX, number) is None:
        abort(400, 'number provided was not in phone number format')


if __name__ == '__main__':
    app.run(debug=True)
