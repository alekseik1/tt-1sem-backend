from flask import request, jsonify, make_response, render_template
from app import app
import json


@app.route('/')
@app.route('/<string:name>/')
def index(name="world"):
    return "Hello, {}".format(name)


def create_stub_answer(request, status_code):
    response_dict = {
        'status_code': status_code,
        'mimetype': 'text/json',
        'method': request.path
    }
    response = app.response_class(
        response=json.dumps(response_dict),
        status=response_dict.get('status_code', 404),
        mimetype=response_dict.get('mimetype', 'text/json')
    )
    return response


@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return """
        <html><head></head><body>
        <form method="POST" action="/form/">
            <input name="first_name" >
            <input name="last_name" >
            <input type="submit" >
        </form>
        </body></html>
        """
    else:
        rv = jsonify(request.form)
        return rv


@app.route('/get_user_chats/<string:user>/', methods=['GET'])
@app.route('/get_user_chats/<string:user>', methods=['GET'])
def get_user_chats(user="Nobody"):
    """
    Чаты пользователя
    """
    return create_stub_answer(request, 200)


@app.route('/get_user_contacts/<string:user>/', methods=['GET'])
@app.route('/get_user_contacts/<string:user>', methods=['GET'])
def get_user_contacts(user="Nobody"):
    """
    Контакты пользователя
    """
    return create_stub_answer(request, 200)


@app.route('/create_chat/<string:chatname>/', methods=['POST'])
@app.route('/create_chat/<string:chatname>', methods=['POST'])
def create_chat(chatname="topsecret"):
    """
    Создать чат
    """
    return create_stub_answer(request, 200)
