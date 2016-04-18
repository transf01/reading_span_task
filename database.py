import sqlite3


class Database():
    def __init__(self, file=None):
        self.db_initialize(file)
        self.make_table()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def db_initialize(self, file):
        file_name = file
        if file_name is None:
            file_name = 'result.db'
        self.db = sqlite3.connect(file_name)
        self.cursor = self.db.cursor()

    def make_table(self):
        self.cursor.execute("create table if not exists user(id TEXT PRIMARY KEY, user_number TEXT, phone TEXT)")
        self.cursor.execute("create table if not exists response(group_code TEXT, sentence_index INTEGER, position TEXT, word TEXT, rt INTEGER, is_correct TEXT, id TEXT, FOREIGN KEY(id) REFERENCES user(id))")

    def set_user(self, user_id):
        self.user_id = user_id

    def add_user(self, user_id, user_number, phone):
        self.set_user(user_id)
        self.cursor.execute("insert into user(id, user_number, phone) values('%s', '%s', '%s')" %(user_id, user_number, phone))
        self.db.commit()

    def add_response(self, word):
        self.cursor.execute("insert into response values('%s', '%s', '%s', '%s', %d, '%s', '%s')"%(word.group, word.index, word.position, word.text, word.rt, word.is_correct_response, self.user_id))
        self.db.commit()

    def clear(self):
        self.cursor.execute("drop table user")
        self.cursor.execute("drop table response")
        self.make_table()