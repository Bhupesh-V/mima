DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  name TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  likes INTEGER DEFAULT 0,
  views INTEGER DEFAULT 0,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  caption TEXT NOT NULL,
  image_url TEXT,
  image_file_id TEXT,
  hashtags TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
