# mysqlpatch.py

## Overview

Managing database state with version control is sometimes challenging. It is helpful to control database changes by creating sql files containing the schema change or data updates.  These sql files are then executed in a prescribed order to roll forward the database.  A table named meta_sql_patch is used to record each sql script that was executed.

This approach allows the developer/administrator to:
- Determine the update status of the database by querying the meta_sql_patch table.
- Apply new changes by dropping sql files into a folder and executing mysqlpatch.py

The objectives of this small python script is to do the following:
- Create meta_sql_patch if it does not yet exist in the target database.
- Read the sql files from a specified directory and execute each if not found in meta_sql_patch.
- Record the execution of each sql script by inserting the file name, date, and success/failure result into meta_sql_patch table.

## Prerequisites

MySQLdb python library
http://mysql-python.sourceforge.net/

Currently, this script has been tested with:
- python 2.7.3
- MySQL 5.5.34
- Ubuntu 12.04.1

## Road Map

Future possible enhancements might include...
- command line arguments


