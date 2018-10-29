from flask import request, jsonify
from app import model
from app import app


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


if __name__ == '__main__':
    app.run()
