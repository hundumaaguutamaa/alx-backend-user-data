#!/usr/bin/env python3
""" Function that returns the log message obfuscated."""
imoprt re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Messages n the fields.
    """
     for field in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message
