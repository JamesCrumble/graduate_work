from fastapi import APIRouter

from ..schemas import Tokens, UserHistoryRecord, UserProfile
from ..schemas.user import RequestSuccess
from .login import user_login
from .logout import user_logout
from .refresh import user_token_refresh
from .sign import user_sign
from .user_history import user_history

router = APIRouter(prefix='/users')
router.add_api_route('/login', user_login, methods=['POST'], response_model=Tokens)
router.add_api_route('/refresh', user_token_refresh, methods=['POST'], response_model=Tokens)
router.add_api_route('/sign', user_sign, methods=['POST'], response_model=UserProfile)
router.add_api_route('/logout', user_logout, methods=['POST'], response_model=RequestSuccess)
router.add_api_route('/user_history', user_history, methods=['GET'], response_model=list[UserHistoryRecord])
