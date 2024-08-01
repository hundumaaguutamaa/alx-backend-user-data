#!/usr/bin/env python3

import re
from typing import List

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
    return re.sub(r'({})=[^{}]*'.format('|'.join(re.escape(field) for field in fields),
                                        re.escape(separator)),
                  lambda m: m.group(0).split('=')[0] + '=' + redaction, message)
