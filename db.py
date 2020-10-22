import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
print('>> Connection to SQLite established...')

# cursor.execute('DROP TABLE users')
# cursor.execute('DROP TABLE connections')

class db:

    def __init__(self):
        try:
            cursor.execute("""CREATE TABLE data (
                                     user_id INTEGER,
                                     dict_0 BOOL,
                                     dict_1 BOOL,
                                     dict_2 BOOL,
                                     dict_3 BOOL,
                                     poshuk BOOL,
                                     page INTEGER, 
                                     current_trnslt STRING)
                                     """)
            conn.commit()
            print('>> >> data table was created')
        except:
            pass
        print('>> >> data table is connected')

    def add_user(self, user_id):
        query = 'INSERT INTO data(user_id, dict_0, dict_1, dict_2, dict_3, poshuk, page) VALUES (%d, 1, 0, 0, 0, 1, 0)' % (user_id)
        cursor.execute(query)
        conn.commit()

    def update(self, user_id, param, value):
        if param not in ['page', 'current_trnslt']:
            value %= 2
        if param == 'current_trnslt':
            value = '"' + value + '"'
        query = "UPDATE data SET %s = '%s' WHERE user_id = %d" % (str(param), str(value), user_id)

        # print('| | | on update: ', query)

        cursor.execute(query)
        conn.commit()

    def get_user(self, user_id):
        query = 'SELECT * FROM data WHERE user_id = %d' % user_id
        cursor.execute(query)
        data = cursor.fetchone()
        if data is not None:
            return list(data)
        else:
            return None



# u_db = u_table()
# c_db = c_table()
#
# u_db.add_user(1234)
# u_db.add_user(12333)
# u_db.display_table()

# conn.commit()
# print(slite.get_user('123'))
# slite.delete_user(123)
# slite.display_users()