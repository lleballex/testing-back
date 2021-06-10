from testing.settings import SECRET_KEY
from testing.settings import ENCRYPTION_ALGORITHM as ALGORITHM

import jwt


def decode_jwt_token(token):
	try:
		return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
	except jwt.exceptions.DecodeError:
		return None

def encode_jwt_token(data):
	return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)