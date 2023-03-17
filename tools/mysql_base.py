import pymysql


class ProjectMysql:
    def __init__(self, database):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = 'abcd123456'
        self.database = database
        self.dbs = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.cursor = self.dbs.cursor()

    def select_data(self, sql):
        self.cursor.execute(sql)
        try:
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            self.dbs.rollback()
            return e

    def close_search(self):
        self.cursor.close()
        self.dbs.close()
