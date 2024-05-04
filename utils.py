# lets use utils for adding additional functionalities to application.

import secrets
from datetime import datetime


# lets write function to genrate jwt secret key
def genrate_jwt_secret_key(no_bits):
    # no_bits should be based on how much secure key we need. the more the bigger no the more secure and long key.
    jwt_secret_key = secrets.token_hex(no_bits)
    
    return jwt_secret_key


