import re


def check_empty_strings(*args):
    for i in args:
        if re.match(r'^[\s]*$', i):
            return False
    return True

print(check_empty_strings('sds', '    '))