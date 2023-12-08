import os

from dotenv import load_dotenv


def init_env() -> None:
    dir = os.path.dirname(os.path.abspath(__file__))
    proj_root = os.path.abspath(os.path.join(dir, '..'))

    test_path = os.path.join(proj_root, '.env.dev.test')
    if os.path.isfile(test_path):
        load_dotenv(dotenv_path=test_path)
        return None
