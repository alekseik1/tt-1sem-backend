from flask import request, jsonify
from app import app
from app import model
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


@app.route('/messages/')
def messages():
    chat_id = int(request.args.get('chat_id'))
    messages = model.list_messages_by_chat(chat_id, 10)
    return jsonify(messages)


@app.route('/find_user/')
def find_user():
    user_name = request.args.get('user_name', None, type=str)
    users = []
    if user_name:
        users = model.find_user(user_name=user_name)
    nick = request.args.get('nick', None, type=str)
    if nick:
        users = model.find_user(nick=nick)
    user_id = request.args.get('user_id', None, type=int)
    if user_id:
        users = model.find_user(user_id=user_id)
    return jsonify(users)


@app.route('/create_chat/', methods=['POST', 'GET'])
def create_chat():
    topic = str(request.args.get('topic'))
    is_group_chat = int(request.args.get('is_group'))
    chat_id = model.create_chat(topic, is_group_chat)
    return jsonify({
        'topic': topic,
        'is_group_chat': is_group_chat,
        'chat_id': chat_id
    })
