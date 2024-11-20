from flask import Flask, jsonify, render_template, request
import time
import random

strings = [
    "String 1",
    "String 2",
    "String 3",
    "String 4",
    "String 5",
    "String 6",
    "String 7",
    "String 8",
    "String 9",
    "String 10"
]


def get_random_string():
    return random.choice(strings)


app = Flask(__name__)


# Main page route
@app.route('/')
def main_page():
    return render_template('index.html')


# This function will be the one to provide the user's answer to the AI and give the UI a response.
@app.route('/get_data', methods=['GET'])
def get_data():
    name = request.args.get('name')
    print(name)
    ##################################
    # Test                           #
    data = {'message': get_random_string(), 'status': 'success'}
    time.sleep(2)
    ##################################
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
