import json
import string
import random
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

def generate_code(prefix, string_length):
    letters = string.ascii_uppercase
    return prefix + ''.join(random.choice(letters) for i in range(string_length))