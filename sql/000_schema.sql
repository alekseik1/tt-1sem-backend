CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    nick TEXT NOT NULL UNIQUE
        CHECK (length(nick) < 32),
    name TEXT NOT NULL
        CHECK (length(name) < 32),
    avatar TEXT NOT NULL
);

CREATE TABLE chats (
  chat_id SERIAL PRIMARY KEY,
  is_group_chat INTEGER,
  topic TEXT NOT NULL
    CHECK (length(topic) < 1000),
  added_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    chat_id INTEGER NOT NULL
      REFERENCES chats(chat_id),
    user_id INTEGER NOT NULL
        REFERENCES users(user_id),
    content TEXT NOT NULL
        CHECK (length(content) < 65536),
    added_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE members (
  user_id INTEGER NOT NULL
    REFERENCES users(user_id),
  chat_id INTEGER NOT NULL
    REFERENCES chats(chat_id),
  new_messages TEXT NOT NULL,
  last_read_message_id INTEGER
    REFERENCES messages(message_id)
);

CREATE TABLE attachments (
  attach_id SERIAL PRIMARY KEY,
  chat_id INTEGER NOT NULL
    REFERENCES chats(chat_id),
  user_id INTEGER NOT NULL
    REFERENCES users(user_id),
  message_id INTEGER NOT NULL
    REFERENCES messages(message_id),
  type TEXT NOT NULL
    CHECK (length(type) < 1000),
  url TEXT NOT NULL
);