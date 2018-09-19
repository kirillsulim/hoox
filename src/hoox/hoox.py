import argparse
import sys
import os
from subprocess import call
from pkg_resources import resource_string

HOOX_DIR = 'hoox'
DEFAULT_FOLDER = os.path.join('..', '..', HOOX_DIR)


def main():
    main_parser = argparse.ArgumentParser(description='')
    main_parser.add_argument('command', nargs=1)
    main_parser.add_argument('options', nargs=argparse.REMAINDER)

    main_args = main_parser.parse_args()

    func_name = main_args.command[0].replace('-', '_')
    func = getattr(get_current_module(), func_name, None)
    if not callable(func):
        print('Unknown command {}'.format(main_args.command))
        exit(1)
    exit(func(main_args.options))


def get_current_module():
    module_name = globals()['__name__']
    return sys.modules[module_name]


def init(args):
    if not os.path.exists(DEFAULT_FOLDER):
        os.makedirs(DEFAULT_FOLDER)
    call(['git', 'config', '--local', 'core.hooksPath', DEFAULT_FOLDER])


def enable(args):
    hook = 'pre-commit'
    data = resource_string('hoox.resources', 'hook-runner.sh').decode('utf8')
    data = data.replace('{{hook-name}}', hook)
    with open(os.path.join(HOOX_DIR, hook), 'wb') as file:
        file.write(data.encode('utf8'))


def run_hook(args):
    print('run-hook called with:', *args)
    exit(0)


if __name__ == '__main__':
    main()
