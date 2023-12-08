'''Usually auth service already builded up somewhere. Building this for tests purpuses is too much...'''

import uuid
from calendar import timegm
from datetime import datetime, timedelta, timezone

import jwt

PRIVATE_KEY: str = '''
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA7l3gk5IZud5An4xDeZbrNG2me4bp1dQJ/QD08CmGZgvDRKD7
pyIVicQib5t51B6Qlw/R4lMC0AA4yiHTSMx7wHe3uch/W8r4GkuZDa4QRAMlGkxv
f3MoAZYHuGHUoBuVVayk0baL6I2pGVZwAGguA+A4K6XQC6ERtgFspjTtjizrB1Gr
stlu1HgWO2ZD6QR0byloLiySf3h2a4B42kJRfiYiV0fVLAJQLqnpt/STbGWUCzjD
FsoRR43C0zjCVKQconDXk82Zc+p4t1cIV3yE+bHLweFQ/vRIOrNza9kxo17bj8LC
OvazUFXT4CqMEDvaO4Texx6QNwC6cYwr4TszkQIDAQABAoIBAHEI54RTVgvED1UZ
iK3SGXtlO/t8AMs7n/jwSTbSGj+t+E1FIdEh4qDP95yBWAZ08BASmm7++mh0knmY
DL+K6Gxe2SsqnuqCl6CwlMXd8yytaRzNflor257U7JhNHC1Ip0pXcllYfYQsGTJA
wSAQRzHjU/+uw7egC+wJROKUWsp+LBDgViQjYJikzhWpzVVzyUvm0WD2gTwlhOrG
oEvZn96E+7cWaw/Im5C94n+wru21dsgmH1xf22yVhv6Zb8iHuZcUVpHSRvAY4lS2
bI/lONfXpI3wRUJLwdwRk4CCg0KFw8mAb4dopPs+mffo1yWcwp3SkIPOpwip4WpF
uz2F7bkCgYEA/7jSfW0K2uZ9WBwTEwEsXpNFzz39RU8CqbKiuWM4OiXT7iOPDpJW
Ks+N6gUW5afNGWE+EugMAk6A9sKHHXfA8mSiwdWk4leFTfvQPDfve7SnYmd//MVT
6e05/o9NIySZNGKWRPLoJc0gSowIAwOZ8AkwDBIviuKBfPMwSK4hkFsCgYEA7qA5
b2BvGd5ZlNU9QUmg59CWI7CTtoob8CPn66Ey4oJwmQbHG4aMTkiTmEH4wg+/9wSd
j5dyB448oGgBk3MKp2BellOLYDhrigJHcRTgik6bw6uxQRfk97dcoRyd8zRhZu5n
R21SNghtQqGw5pr1PeqGZIEtVmyPGsvx+c8bD4MCgYEAgDnO4jGxRb5Zj7rUHa1y
8CFs2dQ9kWli7nCyg78qzI13TWvrKeVa67CTeor+xj1z7IwEMjrE+sseg51bXv1T
dLfdnNBiE1TLdSUVb3ykyyT04bUASmEwCJZ5hBmbFkodwFTHAN/EZGANFxRMWCaQ
I/qXaxYbXMrjHyJaTbdzAQ0CgYEAg4BgpnQqRcM28sIgo54Dwjw8wSZKAMpTYx8m
a7/F3vWrP2lwyEZ5g5qTW9DfWXJ8g5BTlBINkQRdfLhURgGb2WlONuGLaVcuTDu9
SyAKLa3sQQSZBho44Bp4PYEbui8fji3LVJ12NLioHZQlfK/gfmKD9VcKuRnSMx45
F0V+0CkCgYEA4j8E5FUQTBDfzAsJq+swVJ1NhgamzVQxuCILTAJJH2Nf/naApoZV
Jno+qMZIA7ojmg9lAWYy00s1ExDtIPJWgRS/+EbeYtqNKck6cRRprtm10WDGOj7X
YVnh7owyulzSodwGbngXtCsp/eK204YhhPgZhfnvKN+YtlnAoFFEBho=
-----END RSA PRIVATE KEY-----
'''

PRIVATE_KEY = PRIVATE_KEY.encode('utf-8')

TEST_USER_ID: str = str(uuid.uuid4())
TEST_USER_GUEST_ID: str = str(uuid.uuid4())

test_user_token: str = jwt.encode({
    'user_id': TEST_USER_ID,
    'exp': timegm((datetime.now(timezone.utc) + timedelta(minutes=30)).utctimetuple()),
    'iat': timegm(datetime.now(timezone.utc).utctimetuple())
}, PRIVATE_KEY, algorithm='RS256')

test_user_guest_token: str = jwt.encode({
    'user_id': TEST_USER_GUEST_ID,
    'exp': timegm((datetime.now(timezone.utc) + timedelta(minutes=30)).utctimetuple()),
    'iat': timegm(datetime.now(timezone.utc).utctimetuple())
}, PRIVATE_KEY, algorithm='RS256')

if __name__ == '__main__':

    test_user_token: str = jwt.encode({
        'user_id': 'a0a4dfd8-6994-43ae-a670-b9c2502c9bbd',
        'exp': timegm((datetime.now(timezone.utc) + timedelta(minutes=180)).utctimetuple()),
        'iat': timegm(datetime.now(timezone.utc).utctimetuple())
    }, PRIVATE_KEY, algorithm='RS256')
    print(test_user_token)
