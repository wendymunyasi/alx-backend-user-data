#!/usr/bin/env python3
"""Module for personal data project
"""


import logging
import os
import mysql.connector
import re
from typing import List


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class

    Update the class to accept a list of strings fields constructor argument.
    Implement the format method to filter values in incoming log records using
    filter_datum. Values for fields in fields should be filtered.
    DO NOT extrapolate FORMAT manually. The format method should be less than
    5 lines long.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the class.

        Args:
            fields (List[str]): The fields.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum.

        Args:
            record (logging.LogRecord): Values to be filtered.

        Returns:
            str: The filtered values.
        """
        msg = super(RedactingFormatter, self).format(record)
        text = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return text


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
) -> str:
    """Returns the log message obfuscated.

    Args:
        fields (List[str]): a list of strings representing all fields to
        obfuscate.
        redaction (str): a string representing by what the field will be
        obfuscated.
        message (str): a string representing the log line.
        separator (str): a string representing by which character is separating
        all fields in the log line (message).

    Returns:
        str: the log message obfuscated.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object.

    The logger should be named "user_data" and only log up to logging.INFO
    level.
    It should not propagate messages to other loggers. It should have a
    StreamHandler with RedactingFormatter as formatter.
    Create a tuple PII_FIELDS constant at the root of the module containing
    the fields from user_data.csv that are considered PII. PII_FIELDS can
    contain only 5 fields - choose the right list of fields that can are
    considered as “important” PIIs or information that you must hide in your
    logs. Use it to parameterize the formatter.

    Returns:
        logging.Logger: Object.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database
    (mysql.connector.connection.MySQLConnection object.

    You will connect to a secure holberton database to read a users table.
    The database is protected by a username and password that are set as
    environment variables on the server named PERSONAL_DATA_DB_USERNAME,
    (set the default as “root”), PERSONAL_DATA_DB_PASSWORD (set the default
    as an empty string) and PERSONAL_DATA_DB_HOST (set the default as
    “localhost”).
    The database name is stored in PERSONAL_DATA_DB_NAME.

    Returns:
        mysql.connector.connection.MySQLConnection: Connector to the
        database.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection
