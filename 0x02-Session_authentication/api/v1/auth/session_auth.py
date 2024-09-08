#!/usr/bin/env python3
"""Create SessionAuth Flow"""

import uuid
from .auth import Auth


class SessionAuth(Auth):
    """Session Auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Generate session id for current user"""
        if type(user_id) == str:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None
