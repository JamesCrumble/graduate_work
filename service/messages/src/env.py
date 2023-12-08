import os

from dotenv import load_dotenv


def init_env():
    dir = os.path.dirname(os.path.abspath(__file__))
    proj_root = os.path.abspath(os.path.join(dir, '..'))

    prod_path = os.path.join(proj_root, 'secrets', '.env.prod')
    if os.path.isfile(prod_path):
        load_dotenv(dotenv_path=prod_path)
        return

    dev_path = os.path.join(proj_root, 'secrets', '.env.dev')
    if os.path.isfile(dev_path):
        load_dotenv(dotenv_path=dev_path)
        return
