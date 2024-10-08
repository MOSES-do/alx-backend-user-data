#!/usr/bin/env python3
"""Basic Authentication module API"""
import re
import base64
import binascii
from typing import TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Auth BluePrint"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if type(authorization_header) == str:
            """regex exp checking for keyword 'Basic' and other space
                separated value(capture group)"""
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decode base64 encoded auth header """
        if type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """return a tuple of elements"""
        if type(decoded_base64_authorization_header
                ) == str and ':' in decoded_base64_authorization_header:
            username,\
                    password =\
                    decoded_base64_authorization_header.split(':', 1)
            return username, password
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Validate user credential submission in database"""
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
                if len(users) <= 0:
                    return None
                if users[0].is_valid_password(user_pwd):
                    return users[0]
            except Exception:
                return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieve user from a request"""
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
