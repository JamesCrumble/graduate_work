import os
import sys

from env import init_env
from pytest import main

init_env()

if __name__ == '__main__':
    dir = os.path.dirname(os.path.abspath(__file__))
    main_path_test = 'src'
    path_to_test = os.environ.get('PATH_TO_TEST')
    if path_to_test:
        main_path_test = path_to_test
    args: list[str] = [
        '-s',
        '-p',
        'no:cacheprovider',
        os.path.join(dir, main_path_test),
    ]
    exit_code = main(args)
    sys.exit(exit_code)
