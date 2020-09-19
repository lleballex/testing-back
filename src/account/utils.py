from testing.settings import SECRET_KEY

import jwt


def decode_jwt_token(token):
	try:
		return jwt.decode(token, SECRET_KEY)
	except jwt.exceptions.DecodeError:
		return None