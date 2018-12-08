# hoox

Hoox is git hooks manager

## Initialization

For initialization you shuld run init command in project root

```plaintext
hoox init
```

Optional arguments:

- `--directory` or `--d` - directory to store hook scripts. Default is `.hoox` in project root.

You can use separate directory to store typical hooks for specific programming language.

In case of already initialized repository you will be prompted to rewrite hoox directory.

## Show information

To show current hoox status, hoox directory and enabled hooks, you can run following command

```plaintext
hoox info
```

Command will show info:

```plaintext
Hoox dir: ./hoox
Enabled hooks:
  pre-commit
  pre-push
```

## List of supported hooks

Hoox support folowing hooks in current version:

- pre-commit
- pre-push
- commit-msg
- prepare-commit-msg

## Run hook

You can run hook for test purpose via

```plaintext
hoox run-hook <hook-name> [hook-arguments ...]
```

## Enabling hooks

By default all hooks are disabled. To enable hook run

```plaintext
hoox enable <hook-name>
```

Enable hooks realized via adding .sh script that runs `hoox run-hook <hook-name> [hook-arguments]`.

## Disabling hooks

To disable hook run

```plaintext
hoox disable <hook-name>
```

Disable hooks realized via deleting .sh script from previous paragraph.
Do not edit those scripts, cause you can lost all changes when hook is disabled.
