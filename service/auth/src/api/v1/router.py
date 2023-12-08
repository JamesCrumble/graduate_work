from fastapi import APIRouter

from .oauth import oauth_router
from .profile import profile_router
from .roles import roles_router
from .roles.user_role import user_roles_router
from .users import router as users_router

router = APIRouter()
router.include_router(profile_router)
router.include_router(users_router)
router.include_router(roles_router)
router.include_router(user_roles_router)
router.include_router(oauth_router)
