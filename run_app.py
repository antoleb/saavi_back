import json

from flask import Flask, send_file
from markupsafe import escape

from data_analisys.data_analyser import DataAnalyser

app = Flask(__name__)
data_analyser = DataAnalyser()


@app.route('/user/<user_id>')
def show_user_profile(user_id):
    user_info = data_analyser.get_user_info(int(escape(user_id)))
    return json.dumps(user_info)


@app.route('/user/insides/<user_id>/<date>/<type>')
def show_user_insides(user_id, date, type):
    # date: yyyy-mm-dd
    user_insides = data_analyser.get_insides(int(escape(user_id)), escape(date), escape(type))
    return json.dumps(user_insides)


@app.route('/user/popular_categories/<user_id>/<date>/<type>')
def show_user_popular_categories(user_id, date, type):
    # date: yyyy-mm-dd
    user_insides = data_analyser.get_popular_categories(int(escape(user_id)), escape(date), escape(type))
    return json.dumps(user_insides)


@app.route('/user/subscription_prediction/<user_id>/')
def subscription_prediction(user_id):
    user_insides = data_analyser.get_user_subscrption_prediction(int(escape(user_id)))
    return json.dumps(user_insides)


@app.route('/user/active_subscriptions/<user_id>/')
def active_subscriptions(user_id):
    user_insides = data_analyser.get_active_subscriptions(int(escape(user_id)))
    return json.dumps(user_insides)


@app.route('/user/next_two_subscriptions/<user_id>/')
def next_two_subscriptions(user_id):
    user_insides = data_analyser.get_next_two_subscriptions(int(escape(user_id)))
    return json.dumps(user_insides)


@app.route('/images/<name>')
def send_image(name):
    return send_file(f"resourses/{name}")

@app.route('/user/stories/<user_id>')
def send_stores(user_id):
    result = [{
        'm': '/images/3.png',
        's': '/images/5.png',
        't': '/images/1.png',
        'sv': 'https://github.com/azimin/JustVideo/raw/master/Stor2.mp4',
        'si': '/images/4.png',
    }]
    return json.dumps(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0")