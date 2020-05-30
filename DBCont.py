import psycopg2
import sys
import re
import time
"""
    tables : wordList,cpWordList
    func : db.txt, backupDB, plusWord, removeWord, init
        wordList : save word that will be going to use to game 
        cpWordList : copy the wordList & plus colum used, drop table when the game is done
        db.txt : word to backup wordList
        backupDB : backupDB using db.txt
        plusWord : plus word to wordList(table)
        removeWord : remove word in wordList(table)
"""
class DBCont:
    conn_string = "host='localhost' dbname ='kkutuhack' user='kkutuhackuser' password='hackhack'"
    try :
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
    except Exception as e:
        print ("database error")
        sys.exit()
    def excuteQuery(self,sql):
        try:
            connExcute = psycopg2.connect(self.conn_string)
            ExcuteCur = connExcute.cursor()
            ExcuteCur.execute(sql)
            connExcute.commit()
            
            ExcuteCur.close()
            connExcute.close()
            print("query done")
        except Exception as e:
            print(e)

    def createTable(self,TName,colums):
        # colum : array of dict 
        # ex ) colums = [{CName:'colum_name', CType : 'varchar(50)', CProperty : 'UNIQUE NOT NULL'}]
        Processed_col = ""
        try:
            for i,c in enumerate(colums):
                Processed_col += c['CName'] +" "+c['CType']+" "+c['CProperty']+" "
                if (i != len(colums)-1):
                    Processed_col+=", \n"
            print (Processed_col)

            sql = """
                create table """+ TName +"""(
                    """+Processed_col+"""
                );
            """
            self.excuteQuery(sql=sql)
        except Exception as e:
            print(e)
            time.sleep(5)
    def dropTable(self,TName):
        try:
            sql = """ 
                drop table """+TName+""";
            """
            print(sql)
            connExcute = psycopg2.connect(self.conn_string)
            ExcuteCur = connExcute.cursor()
            print("drop plz")
            ExcuteCur.execute(sql)
            print("drop plz")
            connExcute.commit()
            print("drop table success")
            ExcuteCur.close()
            connExcute.close()

        except Exception as e:
            print(e)
            print("error at dropTable")
    def showAllFromTable(self,TName):
        sql = " SELECT * FROM "+TName+";"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
    def insertData(self,TName,data):
        try:
            Processed_data = ""
            for i,d in enumerate(data):  
                if type(d) == type("string"):
                    Processed_data += "'"+d+"'"
                if(len(data)-1 != i):
                    Processed_data += ","
            
            # print(Processed_data)
            sql = "INSERT INTO "+TName+" values ("+Processed_data+");"
            # print(sql)
            self.excuteQuery(sql)
        except Exception as e:
            print(e)
            print("error at insertData()")
    def copyTable(self,existTable,newTable):
        try:
            sql = """
                create table """+newTable+""" as select * from """+existTable+""" ;
            """
            self.excuteQuery(sql)
        except Exception as e:
            print(e)
            print("error at copyTable")
    def gameSet(self):
        try:
            print("drop table")
            self.dropTable("cpWordList")
            print("copy table")
            self.copyTable("wordList","cpWordList")
            # conf = ["not null","default false"]
            # self.addColumnTable("cpWordList","isUsed","boolean",conf)
        except Exception as e:
            print(e)
            print("error at gameSet()")
    def addColumnTable(self,TName,CName,DataType,conf):
        try:
            Processed_conf = ""
            for c in conf:
                Processed_conf += c +" "

            sql = """
                alter table """+TName+""" add column """+CName+""" """+DataType+""" """+Processed_conf+"""
            """
            self.excuteQuery(sql=sql)
        except Exception as e:
            print(e)
            print("error at addColumnTable()")
    def find(self,TName,CName,where,limit):
        try:
            sql = """
                select """+CName+""" from """+TName+""" where """+where+""" limit """+str(limit)+""";
            """
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            print(rows)
            if rows == []:
                return ""
            return rows[0][0]
        except Exception as e:
            print(e)
            print("error at find()")
            return ""
    def update(self,TName, where,ToSet):
        try :
            sql = """
                update """+TName+""" set """+ToSet+""" where """+where+""" ;
            """
            # print(sql)
            self.excuteQuery(sql=sql)        
        except Exception as e:
            print(e)
            print("error at update")
    def removeRow(self,TName,where):
        try :
            sql = """
                delete from """+TName+""" where """+where+""" ;
            """
            # print(sql)
            self.excuteQuery(sql=sql)        
        except Exception as e:
            print(e)
            print("error at removeRow")
