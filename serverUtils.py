#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from callerid_endpoint import aviv
from csv_fetcher import init_data, get_by_phone_number, delete_by_phone_number

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
    result = get_by_phone_number(number)
    if len(result) == 0:
        abort(404, "phone number does not exist")
    return result


@app.route('/remove', methods=['POST'])
def remove_phone_number():
    number = (request.args.get('phone_number'))
    delete_by_phone_number(number)
    return make_response({}, 202)


if __name__ == '__main__':
    app.run(debug=True)
