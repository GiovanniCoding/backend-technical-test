import re


def validate_email(email):
    """
    Validate if the given string is a valid email address.
    """
    pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"

    if re.match(pattern, email):
        return True
    else:
        return False
