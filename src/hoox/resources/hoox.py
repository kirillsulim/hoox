# This file will be runned if hooks are enabled


def pre_commit() -> int:
    return 0


def pre_push(repo_name: str, repo_location: str) -> int:
    return 0


def commit_msg(message_file: str) -> int:
    with open(message_file, 'r') as f:
        pass
    return 0


def prepare_commit_msg(message_file: str, source: str=None, sha1: str=None) -> int:
    with open(message_file, 'r') as f:
        content = f.read()
    with open(message_file, 'w') as f:
        f.write(content)
    return 0
