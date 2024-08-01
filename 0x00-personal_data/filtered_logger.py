#!/usr/bin/env python3
import re

def filter_datum(fields, redaction, message, separator):
    return re.sub(r'({})=[^{}]*'.format('|'.join(re.escape(field) for field in fields), re.escape(separator)), 
                  lambda m: m.group(0).split('=')[0] + '=' + redaction, 
                  message)
