from itsdangerous import URLSafeTimedSerializer
from functools import reduce

SECRET_KEY_CONFIRMATION = 'rV2426fsxwNSem15019LaB1ss30mayCddmsg999'
SECRET_KEY_RESET = 'hf7mN6123Gbz08Ghnsfdh67G34Fdvvasj90a112'

SPECIAL_CONFIRMATION_SALT = 'hsdT56NdbsaI89nMdsa66nsdSdvvzxc'
SPECIAL_RESET_SALT = 'hh72NS6324hfsn423msdl9123hsdjgk'

def generate_email_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY_CONFIRMATION)
    return serializer.dumps(email, salt=SPECIAL_CONFIRMATION_SALT)


def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY_RESET)
    return serializer.dumps(email, salt=SPECIAL_RESET_SALT)


def confirm_email_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY_CONFIRMATION)

    try:
        email = serializer.loads(token, salt=SPECIAL_CONFIRMATION_SALT, max_age=expiration)
    except:
        raise Exception("There is a problem with entered token or smth else i dont know)")
    return email


def reset_password_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY_RESET)

    try:
        email = serializer.loads(token, salt=SPECIAL_RESET_SALT, max_age=expiration)
    except:
        raise Exception("There is a problem with entered token or smth else i dont know)")
    return email
