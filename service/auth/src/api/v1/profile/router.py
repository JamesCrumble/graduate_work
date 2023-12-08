from fastapi import APIRouter, status

from .change_password import change_password

router = APIRouter(prefix='/profile', tags=['profile'])
router.add_api_route(
    '/change_password', change_password,
    methods=['POST'], status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'description': '''
                - New password and current password should not be the same
            '''
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': '''
                - User current password invalid
            '''
        },
    }
)
