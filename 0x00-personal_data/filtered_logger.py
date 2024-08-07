#!/usr/bin/env python3

"""
This module provides functionalities to connect to a secure Holberton database,
filter sensitive information from log messages, and log the database records
in a redacted format.
"""

import os
import re
import logging
from typing import List, Tuple
import mysql.connector
from mysql.connector import connection, Error


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replaces occurrences of certain field values in a log message with a redaction string.

    Args:
        fields (List[str]): List of strings representing all fields to obfuscate.
        redaction (str): String representing by what the field will be obfuscated.
        message (str): String representing the log line.
        separator (str): String representing by which character is separating all fields in the log line.

    Returns:
        str: The log message with obfuscated field values.
    """
    return re.sub(
        r'({})=[^{}]*'.format('|'.join(re.escape(field) for field in fields), re.escape(separator)),
        lambda m: m.group(0).split('=')[0] + '=' + redaction,
        message
    )


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for logging.

    Attributes:
        REDACTION (str): The redaction string to use for sensitive information.
        FORMAT (str): The log format string.
        SEPARATOR (str): The separator character for log fields.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.

        Args:
            fields (List[str]): List of fields to redact in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record, redacting specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with redacted fields.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Creates a logger named 'user_data' that logs up to INFO level and does not propagate messages to other loggers.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connects to the MySQL database using credentials from environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection: A MySQLConnection object connected to the database.
    """
    # Retrieve database credentials from environment variables
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    if db_name is None:
        raise ValueError("The environment variable PERSONAL_DATA_DB_NAME must be set.")

    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )
        return connection
    except Error as err:
        raise RuntimeError(f"Error connecting to the database: {err}")


def main() -> None:
    """
    Connects to the database, retrieves all rows from the users table, and displays each row under a filtered format.
    """
    try:
        # Get database connection
        db_connection = get_db()

        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        # Get the logger
        logger = get_logger()

        # Display each row in the specified format
        for row in rows:
            # Construct the log message
            log_message = "; ".join(f"{key}={value}" for key, value in row.items())
            logger.info(log_message)

        # Print the filtered fields
        print("Filtered fields:")
        for field in PII_FIELDS:
            print(field)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the database connection is closed
        if db_connection.is_connected():
            db_connection.close()


if __name__ == "__main__":
    main()
