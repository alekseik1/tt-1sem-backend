from flask import request, jsonify
from app import model
from app import app


@app.route('/messages/')
def messages():
    chat_id = int(request.args.get('chat_id'))
    messages = model.list_messages_by_chat(chat_id, 10)
    return jsonify(messages)


if __name__ == '__main__':
    app.run()
