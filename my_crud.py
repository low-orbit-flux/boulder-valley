
# x create / delete db
# x create / delete table
# x add / remove column
# x insert data
# x remove data
# x update data
# x search / return data
# x list tables
# x list databases

# PK auto increment is only setup for MySQL

# pip install MySQL-python # needs mysql bin in the path and gcc


import MySQLdb


def create_db(db_host, db_user, db_password, db_name):
    con = MySQLdb.connect(db_host, db_user, db_password)
    cur = con.cursor()
    cur.execute('CREATE DATABASE ' + db_name)
    con.commit()
    con.close()


def drop_db(db_host, db_user, db_password, db_name):
    sql_command = 'DROP DATABASE ' + db_name
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    con.commit()
    con.close()


def create_table(db_host, db_user, db_password, db_name, table_name, fields):
    sql_command = 'CREATE TABLE if not exists ' + table_name + ' ( ID int NOT NULL AUTO_INCREMENT PRIMARY KEY, '
    first = True
    for i in fields:
        i_type = i[0]
        i_name = i[1]
        if first:
            first = False
            if i_type == "varchar":
                sql_command = sql_command + ' ' + i_name + ' varchar(255) '
            elif i_type == "int":
                sql_command = sql_command + ' ' + i_name + ' int '
            else:
                return "Error: need type"
        else:
            if i_type == "varchar":
                sql_command = sql_command + ', ' + i_name + ' varchar(255) '
            elif i_type == "int":
                sql_command = sql_command + ', ' + i_name + ' int '
            else:
                return "Error: need type"

    sql_command = sql_command + ' )'
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    con.commit()
    con.close()


def drop_table(db_host, db_user, db_password, db_name, table_name):
    sql_command = 'DROP TABLE ' + table_name
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    con.commit()
    con.close()


def add_col(db_host, db_user, db_password, db_name, table_name, new_col):
    i_type = new_col[0]
    i_name = new_col[1]
    if i_type == "varchar":
        sql_command = 'ALTER TABLE ' + table_name + ' ADD ' + i_name + ' varchar(255)'
    elif i_type == "int":
        sql_command = 'ALTER TABLE ' + table_name + ' ADD ' + i_name + ' int'
    else:
        return "Error: need type"
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    con.commit()
    con.close()


def drop_col(db_host, db_user, db_password, db_name, table_name, new_col):
    sql_command = 'ALTER TABLE ' + table_name + ' DROP COLUMN ' + new_col
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    con.commit()
    con.close()


def insert_data(db_host, db_user, db_password, db_name, table_name, fields):
    sql_command = 'INSERT INTO ' + table_name + ' VALUES (null, '
    first = True
    for i in fields:
        i_type = i[0]
        i_name = i[1]
        if first:
            first = False
            if i_type == "varchar":
                sql_command = sql_command + ' \'' + i_name + '\''
            elif i_type == "int":
                sql_command = sql_command + ' ' + i_name
            else:
                return "Error: need type, got: " + i_type
        else:
            if i_type == "varchar":
                sql_command = sql_command + ', \'' + i_name + '\''
            elif i_type == "int":
                sql_command = sql_command + ', ' + i_name
            else:
                return "Error: need type, got: " + i_type

    sql_command = sql_command + ')'
    #print "\n\n" + sql_command + "\n\n"
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    con.commit()
    con.close()


def delete_data(db_host, db_user, db_password, db_name, table_name, row_id):
    sql_command = 'DELETE FROM ' + table_name + ' WHERE ID = ' + row_id
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    con.commit()
    con.close()


def update_data(db_host, db_user, db_password, db_name, table_name, row_id, field_map):
    sql_command = 'UPDATE ' + table_name + ' SET '
    first = True
    for i in field_map:
        i_type = field_map[i][0]
        i_name = field_map[i][1]
        if first:
            first = False
            if i_type == "varchar":
                sql_command = sql_command + i + '=\'' + i_name + '\''
            elif i_type == "int":
                sql_command = sql_command + i + '=' + i_name
            else:
                return "Error: need type"
        else:
            if i_type == "varchar":
                sql_command = sql_command + ', ' + i + '=\'' + i_name + '\''
            elif i_type == "int":
                sql_command = sql_command + ', ' + i + '=' + i_name
            else:
                return "Error: need type"
    sql_command = sql_command + ' WHERE ID = ' + row_id
    print(sql_command)
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    con.commit()
    con.close()


def print_all(db_host, db_user, db_password, db_name, table_name):
    sql_command = 'SELECT * FROM ' + table_name
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    rows = cur.fetchall()
    con.commit()
    con.close()
    return rows


def search(db_host, db_user, db_password, db_name, table_name, field_map):
    sql_command = 'SELECT * FROM ' + table_name + ' WHERE '
    first = True
    for i in field_map:
        i_type = field_map[i][0]
        i_name = field_map[i][1]
        if first:
            first = False
            if i_type == "varchar":
                sql_command = sql_command + i + '=\'' + i_name + '\''
            elif i_type == "int":
                sql_command = sql_command + i + '=' + i_name
            else:
                return "Error: need type"
        else:
            if i_type == "varchar":
                sql_command = sql_command + ' and ' + i + '=\'' + i_name + '\''
            elif i_type == "int":
                sql_command = sql_command + ' and ' + i + '=' + i_name
            else:
                return "Error: need type"
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    rows = cur.fetchall()
    con.commit()
    con.close()
    return rows


def list_tables(db_host, db_user, db_password, db_name):
    sql_command = 'SHOW TABLES'
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    rows = cur.fetchall()
    con.commit()
    con.close()
    return rows


def list_dbs(db_host, db_user, db_password):
    sql_command = 'SHOW DATABASES'
    con = MySQLdb.connect(db_host, db_user, db_password)
    cur = con.cursor()
    cur.execute(sql_command)
    rows = cur.fetchall()
    con.commit()
    con.close()
    return rows


def describe_table(db_host, db_user, db_password, db_name, table_name):
    sql_command = 'describe ' + table_name
    con = MySQLdb.connect(db_host, db_user, db_password, db_name)
    cur = con.cursor()
    cur.execute(sql_command)
    rows = cur.fetchall()
    con.commit()
    con.close()
    cols = []
    for i in rows:
        cols.append(i[0])
    return cols


def run_stuff():
    #create_db("127.0.0.1", "root", "xxxxxxxx", "asdf")
    fields = ['a', 'b', 'c']
    data = ["fish", "tree", "house"]
    data2 = {'a': 'cloud', 'b':'rock', 'c':'river'}
    data3 = {'b': 'xxxxxx'}
    data4 = {'a': 'cloud'}
    #create_table("127.0.0.1", "root", "xxxxxxxx", "asdf", "zoidberg", fields)
    #add_col("127.0.0.1", "root", "xxxxxxxx", "asdf", "zoidberg", "some_more_junk")
    #drop_col("127.0.0.1", "root", "xxxxxxxx", "asdf", "zoidberg", "some_more_junk")
    #drop_table("127.0.0.1", "root", "xxxxxxxx", "asdf", "zoidberg")
    #drop_db("127.0.0.1", "root", "xxxxxxxx", "asdf")
    #insert_data("127.0.0.1", "root", "xxxxxxxx", "asdf", "zoidberg", data)
    #delete_data("127.0.0.1", "root", "xxxxxxxx", "asdf", "frog", "1")
    #update_data("127.0.0.1", "root", "xxxxxxxx", "asdf", "frog", "5", data2)  # update row id 5 with dict data2
    #print_all("127.0.0.1", "root", "xxxxxxxx", "asdf", "frog")
    #junk = search("127.0.0.1", "root", "xxxxxxxx", "asdf", "frog", data4)
    #print junk
    #junk2 = list_dbs("127.0.0.1", "root", "xxxxxxxx")
    #junk3 = list_tables("127.0.0.1", "root", "xxxxxxxx", "asdf")
    #print "DBs: " + str(junk2)
    #print "Tables in asdf: " + str(junk3)
    #junk3 = describe_table("127.0.0.1", "root", "xxxxxxxx", "test", "test1")
    #print junk3
    results = search("127.0.0.1", "root", "xxxxxxxx", "asdf", "zoidberg", data23)
    print results


#search

if __name__ == "__main__":
    pass
    run_stuff()



