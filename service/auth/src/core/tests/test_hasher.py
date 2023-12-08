from ..hasher import PBKDHasher


def test_hash_pbkd():
    password = 'mypassword'
    hash_password = PBKDHasher().encode(password)
    assert PBKDHasher().check(password, hash_password)
    assert not PBKDHasher().check('pwd', hash_password)
    new_hash = hash_password[32:] + hash_password[:32]
    assert not PBKDHasher().check('mypassword', new_hash)
