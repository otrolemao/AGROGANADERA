"""Puente PyMySQL -> MySQLdb para que Django use el backend de MySQL.

Django espera el modulo MySQLdb (mysqlclient). PyMySQL es un conector puro en
Python con la misma API, asi que basta con registrarlo con el nombre que Django
va a importar.
"""

import pymysql

pymysql.install_as_MySQLdb()
