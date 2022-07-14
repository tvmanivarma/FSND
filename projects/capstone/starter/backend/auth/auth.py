import os
import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

#AUTH0_DOMAIN = 'manifsnd.us.auth0.com'
#ALGORITHMS = ['RS256']
#API_AUDIENCE = 'castingagency'

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get['ALGORITHMS']
API_AUDIENCE = os.environ.get['API_AUDIENCE']

# AuthError Exception
"""
AuthError Exception
A standardized way to communicate auth failure modes
"""
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Auth Header

def get_token_auth_header():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header expected.'
        }, 401)

    header_parts = auth_header.split()
    if header_parts[0].lower() != 'bearer':
        print('Error 01: 401 - Invalid Header, Authorization header must start with  - Bearer!')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer"'
        }, 401)
    elif len(header_parts) == 1:
        print('Error 02: 401 - Invalid Header, Token not found!')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
        }, 401)

    elif len(header_parts) > 2:
        print('Error 03: 401 - Invalid Header, Invalid authorization Header!')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid authorization header'
        }, 401)

    token = header_parts[1]
    return token

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        print('Error 04: 400 - Invalid Claims, Permissions not included in JWT Token!')
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT'
        }, 400)
    if permission not in payload['permissions']:
        print('Error 05: 403 - Unauthorized, Permission not found!')
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        print('Error 06: 401 - Invalid Header, Authorization token malformed!')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization token malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            print('Error 07: 401 - JWT Token Expired!')
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            print('Error 08: 401 - Invalid / Incorrect Claims, check the audience and issuer!')
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            print('Error 09: 400 - Invalid Header, Unable to parse authentication token!')
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                 raise AuthError({
                    'code': 'invalid_token',
                    'description': 'Access denied due to invalid token'
                }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
    