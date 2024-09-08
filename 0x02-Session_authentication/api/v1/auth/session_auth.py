#!/usr/bin/env python3
"""Create SessionAuth Flow"""

import uuid
from .auth import Auth
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return User_ID based on a session id"""
        if type(session_id) == str:
            if session_id in self.user_id_by_session_id:
                user_id = self.user_id_by_session_id.get(session_id, None)
                return user_id
        return None

    def current_user(self, request=None):
        """Retrieves the user associated with the request.
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)
