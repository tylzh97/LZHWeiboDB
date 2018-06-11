#!/usr/bin/python
# -*- coding: utf-8 -*-


import pymysql


class MySqlService:
    '''This is a class for USING MYSQL'''
    def __init__(self, dbName):
        self.db = None
        self.dbName  = dbName
        self.initialization()

    def initialization(self):
        self.db = self.connectMysql(host = 'localhost', userName = 'root', passWD = 'tylzh1997', database = self.dbName)


        #The Function to connect MySQL Database
    def connectMysql(self, host = 'localhost', userName = 'root', passWD = 'tylzh1997', database = ''):
        return pymysql.connect(host, userName, passWD, database, charset='utf8')

        #The Function to close the connection to MySQL
    def closeMysql(self):
        self.db.close()

        #This is a Function to check the Version of MySQL
    def checkVersions(self):
        cursor = self.db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()
        return "Database version : %s " % data

        #This is a Function to create databases for db
    def createDatabase(self, dbName , sVariable, sConstraint):
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = self.db.cursor()
            # 使用 execute() 方法执行 SQL，如果表存在则删除
            cursor.execute("DROP TABLE IF EXISTS %s" %dbName)
            # 使用预处理语句创建表
            sql = "CREATE TABLE " + dbName + ' ' + sVariable + ' ' + sConstraint + ';'
            cursor.execute(sql)
            return True
        except:
            return False

        #This is a Function to insertMessage into MySQL db
    def insert(self, insertSQL):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 插入语句
        sql = insertSQL
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return True
        except:
            # 如果发生错误则回滚
            self.db.rollback()
            return False
        
        #This is a Function to SELECT MySQL db
    def select(self, sql = ''):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            return results
        except:
            return False

        #This is a Function to UPDATE data
    def updateDatabase(self, updateSQL):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 更新语句
        sql = updateSQL
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return True
        except:
            # 发生错误时回滚
            self.db.rollback()
            return False

        #This is a Function to DELETE data
    def deleteTuple(self, tableName, condition):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 删除语句
        sql = "DELETE FROM " + tableName + " WHERE " + condition + ';'
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            self.db.commit()
            return True
        except:
            # 发生错误时回滚
            self.db.rollback()
            return False

    def runSQL(self, sql):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            self.db.commit()
            return results
        except:
            self.db.rollback()
            return False



if __name__ == '__main__':
    print("Hello world!")
    #This is MAIN FUNCTION



























































































