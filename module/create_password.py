import secrets
import string


def pass_gen(size=8):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    chars += '%&$#()'
    return ''.join(secrets.choice(chars) for x in range(size))
