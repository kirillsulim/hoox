import argparse
import sys
import os
import os.path as path
import stat
from subprocess import call, run, PIPE
from pkg_resources import resource_string
from inspect import getmembers, isfunction, getmodule
from typing import List

DEFAULT_HOOX_DIRECTORY = path.join('.', 'hoox')
HOOX_FILE = 'hoox.py'

NOT_A_GIT_REPO_ERROR_MESSAGE = 'Current directory is not a git repository'


def main():
    if not _check_in_git_repo():
        print(NOT_A_GIT_REPO_ERROR_MESSAGE)
        exit(1)

    main_parser = argparse.ArgumentParser(description='')
    main_parser.add_argument('command', nargs=1, choices=_get_available_commands())
    main_parser.add_argument('options', nargs=argparse.REMAINDER)

    main_args = main_parser.parse_args()

    func_name = _get_function_name(main_args.command[0])
    func = getattr(_get_current_module(), func_name, None)
    if not callable(func):
        print('Unknown command {}'.format(main_args.command))
        print(main_parser.format_help())
        exit(1)
    exit(func(main_args.options))


def init(args: List[str]) -> int:
    init_parser = argparse.ArgumentParser(description='')
    init_parser.add_argument('-d', '--directory', nargs='?', help='hoox directory')

    args = init_parser.parse_args(args)
    directory = args.directory if args.directory else DEFAULT_HOOX_DIRECTORY

    hoox_dir = _get_hoox_dir()
    if hoox_dir:
        res = input('Do you want to reinit and replace from {} to {} directory? [y/N] '.format(hoox_dir, directory)).lower()
        if res != 'y' and res != 'yes':
            print('Aborting init')
            return 0

    if not os.path.exists(directory):
        os.makedirs(directory)
    hoox_file = path.exists(path.join(directory, HOOX_FILE))
    if not path.exists(hoox_file):
        data = resource_string('hoox.resources', 'hoox.py').decode('utf8')
        with open(hoox_file, 'wb') as file:
            file.write(data.encode('utf8'))

    return call(['git', 'config', '--local', 'core.hooksPath', directory])


def enable(args: List[str]) -> int:
    enable_parser = argparse.ArgumentParser(description='')
    enable_parser.add_argument('hook', nargs=1, help='hook name')

    args = enable_parser.parse_args(args)
    hook = args.hook[0]
    if not _check_hook_is_supported(hook):
        print('Hook {} is not supported'.format(hook))
        return 1

    data = resource_string('hoox.resources', 'hook-runner.sh').decode('utf8')
    data = data.replace('{{hook-name}}', hook)
    hook_sh = path.join(_get_hoox_dir(), hook)
    with open(hook_sh, 'wb') as file:
        file.write(data.encode('utf8'))
    os.chmod(hook_sh, os.stat(hook_sh).st_mode | stat.S_IEXEC)

    return 0


def disable(args: List[str]) -> int:
    disable_parser = argparse.ArgumentParser(description='')
    disable_parser.add_argument('hook', nargs=1, help='hook name')

    args = disable_parser.parse_args(args)
    hook = args.hook[0]
    if not _check_hook_is_supported(hook):
        print('Hook {} is not supported'.format(hook))
        return 1

    hook_sh = path.join(_get_hoox_dir(), hook)
    if path.exists(hook_sh):
        os.remove(hook_sh)
        print('Hook {} disabled'.format(hook))
    else:
        print('Hook {} is not enabled'.format(hook))
    return 0


def run_hook(args: List[str]) -> int:
    run_hook_parser = argparse.ArgumentParser(description='')
    run_hook_parser.add_argument('hook_name', metavar='hook-name', nargs=1, help='hook name')
    run_hook_parser.add_argument('args', nargs=argparse.REMAINDER)
    args = run_hook_parser.parse_args(args)

    hook_func = _get_function_name(args.hook_name[0])
    hoox_script = path.join(_get_hoox_dir(), HOOX_FILE)

    with open(hoox_script, 'r') as f:
        code = compile(f.read(), HOOX_FILE, 'exec')
    scope = {}
    exec(code, scope)
    exit_code = scope[hook_func](*args.args)
    if exit_code != 0:
        print('Hook {} exited with code {}'.format(args.hook_name[0], exit_code))
    return exit_code


def info(args: List[str]) -> int:
    hoox_dir = _get_hoox_dir()
    if hoox_dir:
        print('Hoox dir:', hoox_dir)
    else:
        print('Hoox is not initialized for this repository')
        return 0

    enabled_hooks = [f for f in os.listdir(hoox_dir) if path.isfile(path.join(hoox_dir, f)) and _check_hook_is_supported(f)]
    if enabled_hooks:
        print('Enabled hooks:')
        for hook in enabled_hooks:
            print('  ' + hook)
    else:
        print('No enabled hooks')
    return 0


def _get_current_module():
    module_name = globals()['__name__']
    return sys.modules[module_name]


def _get_available_commands() -> List[str]:
    module = _get_current_module()
    return [
        name for name, member in getmembers(module) \
        if getmodule(member) == module \
            and isfunction(member) \
            and not name.startswith('_') \
            and not name == 'main'
    ]


def _get_hoox_dir() -> str:
    result = run(['git', 'config', '--get', 'core.hooksPath'], stdout=PIPE)
    directory = result.stdout.decode('utf8').strip('\n\r\t ')
    return directory


def _check_hook_is_supported(hook: str) -> bool:
    return hook in [
        'pre-commit',
        'pre-push',
        'commit-msg',
        'prepare-commit-msg',
    ]


def _check_in_git_repo() -> bool:
    return path.isdir('.git')


def _get_function_name(name: str) -> str:
    return name.replace('-', '_')


if __name__ == '__main__':
    main()
