#!/usr/bin/env python3
"""Create authentication flow"""

from flask import request
from typing import List, TypeVar



class Auth:
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require Auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization Header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
