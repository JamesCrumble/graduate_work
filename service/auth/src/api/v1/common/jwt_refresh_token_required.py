from curses import wrapper
from datetime import time


class Decorators:

    @staticmethod
    def refresh_token(decorated):
        # the function that is used to check
        # the JWT and refresh if necessary
        @wrapper
        def wrap(api, *args, **kwargs):
            if time() > api.access_token_expiration:
                api.getAccessToken()
            return decorated(api, *args, **kwargs)

        return wrap

    def jwt_refresh_token_required(func):
        @wrapper
        def wrap(*args, **kwargs):
            pass

        return wrap
