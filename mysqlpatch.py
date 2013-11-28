#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import glob
import MySQLdb

def createSqlPatchStatusTable(config):
  try:
    # Connect to MySQL
    conn = MySQLdb.connect (host = config['host'],
                            user = config['user'],
                            passwd = config['pw'],
                            db = config['db'])
    print "createSqlPatchStatusTable.Connected to " + config['db']

    # Execute create table if not exists 
    sql = """create table if not exists meta_sql_patch (
              id int AUTO_INCREMENT primary key NOT NULL,
              sql_filename varchar(1000) not null,
              success int not null,
              InsertDate timestamp default NOW() NOT NULL
              ) engine=InnoDB;"""

    cursor = conn.cursor ()
    result = cursor.execute(sql)
    cursor.close ()
    conn.close ()

  except MySQLdb.Error, e:
    print "Error %d: %s \n" % (e.args[0], e.args[1])
    cursor.close ()
    conn.close ()
    result = -1

  # Return success/failure
  return result

def getSqlFileList(path):
  # List files in directory
  return glob.glob(path + "*.sql")

def readSqlPatchStatus(config):
  try:
    # Connect to MySQL
    conn = MySQLdb.connect (host = config['host'],
                            user = config['user'],
                            passwd = config['pw'],
                            db = config['db'])
    print "readSqlPatchStatus.Connected to " + config['db']

    # Read sql_patch_status table to array
    sql = "select sql_filename from meta_sql_patch;"
    cursor = conn.cursor ()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close ()
    conn.close ()

  except MySQLdb.Error, e:
    print "Error %d: %s \n" % (e.args[0], e.args[1])
    data = ('error',)

  # Return array
  return data

def readSqlFile(filename):
  try:
    # Read sql from file
    f = open(filename, 'r')
    with f:
      sql = f.read()
      return sql
  except Exception, e:
    print "Error reading sql file" + str(e)

def executeSql(config, sql):
  try:
    # Connect to MySQL
    conn = MySQLdb.connect (host = config['host'],
                            user = config['user'],
                            passwd = config['pw'],
                            db = config['db'])
    print "executeSql.Connected to " + config['db']
    #conn.autocommit(True)

    # Here we need to parse the sql to execute as separate individual stmts.
    sqllist = sql.split(";")
    cursor = conn.cursor ()
    for stmt in sqllist:
      if len(stmt.strip()) > 1:
        cursor.execute(stmt)
        conn.commit ()

    # Close the connection and return
    cursor.close ()
    conn.close ()
    result = 1

  except MySQLdb.Error, e:
    #conn.rollback()
    print "Error %d: %s \n" % (e.args[0], e.args[1])
    result = 0

  # Return success/failure
  return result

def insertSqlPatchTable(config, filename, success):
  try:
    # Insert result of sql execution
    # Connect to MySQL
    conn = MySQLdb.connect (host = config['host'],
                            user = config['user'],
                            passwd = config['pw'],
                            db = config['db'])
    print "insertPatchTable.Connected to " + config['db']

    cursor = conn.cursor ()
    result = cursor.execute("""INSERT INTO meta_sql_patch (sql_filename, success) VALUES (%s,%s)""",(filename,success))
    cursor.close ()
    conn.commit ()
    conn.close ()
    result = 1

  except MySQLdb.Error, e:
    print "Error %d: %s \n" % (e.args[0], e.args[1])
    result = 0

  # Return success/failure
  return result 


if __name__ == '__main__':
  # Read args: database_name, sql_file_dir, user, password, host

  # Store config info in a dictionary
  #
  config = {'host': 'localhost', 
            'db'  : 'testdb',
            'user': 'mysqlusername',
            'pw'  : 'mysqlpassword',
            'path': 'mysqlpatch/sql_patch/'}

  # If not exist, create meta_sql_patch table
  #
  createSqlPatchStatusTable(config)

  # Read rows from meta_sql_patch table
  #
  datarows = readSqlPatchStatus(config)
  sqlpatches = []
  for row in datarows:
    sqlpatches.append(row[0])

  # Read and execute each sql file
  #
  sqlfiles = getSqlFileList(config['path'])
  sqlfiles.sort()
  for file in sqlfiles:
    if file in sqlpatches:
      print "already applied: " + file
      continue
    else:
      sql = readSqlFile(file)
      print "read: " + file
      result = executeSql(config, sql)
      print "executed: " + file + "with result = " + str(result)
      insertSqlPatchTable(config, file, result)
      if (result == 1):
        print "execution succeeded: \n" + file
      else:
        print "execute failed: \n" + file



