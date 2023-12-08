from ..core.jwt import JWTTokenPair, UserPayload


def test_jwt():
    user_payload = {'user_id': '12345', 'groups': [1234, 4321], 'browser_fingerprint': '1234'}
    jwt_pair = JWTTokenPair(UserPayload(**user_payload))
    access_payload = JWTTokenPair.verify_jwt_token(f'{jwt_pair.access_token}')
    assert access_payload['user_id'] == user_payload['user_id']

    refresh_payload = JWTTokenPair.verify_jwt_token(f'{jwt_pair.refresh_token}')
    assert refresh_payload['user_id'] == user_payload['user_id']

    assert JWTTokenPair.verify_jwt_token(f'{jwt_pair.refresh_token}f') is None


if __name__ == '__main__':
    test_jwt()
