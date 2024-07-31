import re

def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (list): A list of strings representing all fields to obfuscate.
        redaction (str): A string representing by what the field will be obfuscated.
        message (str): A string representing the log line.
        separator (str): A string representing the character that separates all fields in the log line.

    Returns:
        str: The log message with specified fields obfuscated.
    """
    pattern = '|'.join(f'{field}=[^{separator}]+' for field in fields)
    return re.sub(pattern, lambda m: m.group().split('=')[0] + '=' + redaction, message)

