import sqlite3


class DataBase:
    def __init__(self):
        self.name = {0: "userid", 1: "fullname", 2: "start_data", 3: "referals", 4: "username", 5: "admin", 6: "time"}
        self.conn = sqlite3.connect('test.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
        userid INT PRIMARY KEY,
        fullname TEXT,
        start_data TEXT,
        referals INT,
        username TEXT,
        admin INT,
        time INT,
        count_message INT,
        active INT);""")
        self.conn.commit()

    def addUser(self, user):
        try:
            self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", user)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update(self, index, val, user):
        self.cur.execute(f"UPDATE users SET {index} = {val} WHERE userid = {user};")
        self.conn.commit()

    def userExist(self, user_id):
        self.cur.execute(f"SELECT COUNT(*) FROM users WHERE userid = {user_id}")
        count = self.cur.fetchone()[0]
        if count != 0:
            return True
        else:
            return False
        # self.cur.execute("SELECT userid FROM users")
        # users = self.cur.fetchall()
        # if len(users) != 0:
        #     for i in range(len(users)):
        #         if users[i][0] == user_id:
        #             return True
        #         return False
        # return False

    def getUser(self, user_id):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        if len(users) != 0:
            for i in range(len(users)):
                if users[i][0] == user_id:
                    return users[i]

    def up_sub(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        if len(users) != 0:
            return users

    def getUser_d(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        if len(users) != 0:
            return users[0][2]

    def getUsersID(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        if len(users) != 0:
            count = ''
            for i in range(len(users)):
                count += f'{users[i][0]} '
            return count

    def get_users_start_data(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        if len(users) != 0:
            count = ""
            for i in range(len(users)):
                count += f'{users[i][2]} '
            return count


    def getUsersDATE(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        if len(users) != 0:
            count = ''
            for i in range(len(users)):
                count += f'{users[i][2]} '
            return count

    def checkUser(self, user_id):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        if len(users) != 0:
            for i in range(len(users)):
                if users[i][0] == user_id:
                    return True

    def check_admin(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        count_admin = []
        if len(users) != 0:
            for i in range(len(users)):
                if users[i][5] == 1:
                    count_admin.append(users[i][0])
        return count_admin


    def check_ref(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        count = {"id": '', "username": '', 'ref': '', 'active': ''}
        if len(users) != 0:
            for i in range(len(users)):
                count['id'] += f' {users[i][0]}'
                count['username'] += f' {users[i][4]}'
                count['ref'] += f' {users[i][3]}'
                count['active'] += f' {users[i][8]}'
        print(len(count['active'].split()))
        return count



    def check_date(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        count_date = {"date": '', "username": ''}
        if len(users) != 0:
            for i in range(len(users)):
                count_date['date'] = f'{users[i][2]}'
                count_date['username'] = f'{users[i][4]}'
        return count_date


