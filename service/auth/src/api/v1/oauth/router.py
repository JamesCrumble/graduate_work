from fastapi import APIRouter

from .oauth_service import auth, link, link_perform, login, untie

router = APIRouter(prefix='/oauth')
router.add_api_route('/login/{oauth_type}', login, methods=['GET'])
router.add_api_route('/auth/{oauth_type}', auth, methods=['GET'])
router.add_api_route('/link/{oauth_type}', link, methods=['GET'])
router.add_api_route('/link_perform/{oauth_type}', link_perform, methods=['GET'])
router.add_api_route('/untie/{oauth_type}', untie, methods=['GET'])
