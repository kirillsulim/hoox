import argparse
import sys

DEFAULT_FOLDER = './hoox'


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


def foo(args):
    print("Hi")
    print(args)


if __name__ == '__main__':
    main()
