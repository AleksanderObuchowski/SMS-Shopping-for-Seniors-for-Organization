import random
import string


def random_password():
    chars = string.ascii_letters + string.digits
    stringLength = 6
    return ''.join(random.choice(chars) for i in range(stringLength))