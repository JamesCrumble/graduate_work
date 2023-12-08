# from auth.core.jwt import JWTTokenPair, UserPayload, verify_jwt_token


# def test_jwt():
#     user_payload = {'user_id': '12345', 'groups': [1234, 4321]}
#     jwt_pair = JWTTokenPair(UserPayload(**user_payload))
#     assert verify_jwt_token(f'{jwt_pair.refresh_token}') == user_payload
#     assert verify_jwt_token(f'{jwt_pair.refresh_token}f') is None
# #
