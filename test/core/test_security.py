from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError

from app.core.security import get_current_user
from app.db.models.user import User, UserRepository


class TestGetCurrentUser:
    @pytest.fixture(autouse=True)
    def setup_method(self, request):
        self.mock_user_repo = Mock(spec=UserRepository)
        self.mock_db = Mock()

        patcher_user_repo = patch(
            "app.core.security.UserRepository", return_value=self.mock_user_repo
        )
        patcher_jwt_decode = patch("app.core.security.jwt.decode")

        self.mock_user_repo_patch = patcher_user_repo.start()
        self.mock_jwt_decode_patch = patcher_jwt_decode.start()

        request.addfinalizer(patcher_user_repo.stop)
        request.addfinalizer(patcher_jwt_decode.stop)

        self.mock_user = Mock(spec=User)
        self.mock_user.is_admin = True

    def test_get_current_user_valid_token_and_user_exists(self):
        self.mock_jwt_decode_patch.return_value = {"sub": "testuser"}
        self.mock_user_repo.get_by_username.return_value = self.mock_user

        result = get_current_user("valid_token", self.mock_db)

        assert result == self.mock_user

    def test_get_current_user_valid_token_and_user_not_exists(self):
        self.mock_jwt_decode_patch.return_value = {"sub": "testuser"}
        self.mock_user_repo.get_by_username.return_value = None

        with pytest.raises(HTTPException):
            get_current_user("valid_token", self.mock_db)

    def test_get_current_user_invalid_token(self):
        self.mock_jwt_decode_patch.side_effect = InvalidTokenError

        with pytest.raises(HTTPException):
            get_current_user("invalid_token", self.mock_db)
