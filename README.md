# hoox

Hoox is git hooks manager

## Initialization

For initialization you shuld run init command in project root

```sh
hoox init
```

Optional arguments:

- `--directory` or `--d` - directory to store hook scripts. Default is `.hoox` in project root.

You can use separate directory or eve repository to store typical hooks for specific language.

## List pf supported hooks

Hoox support folowing hooks in current version:

- pre-commit
- pre-push
- commit-msg
- prepare-commit-msg

## Run hook

You can run hook for test purpose via

```sh
hoox run-hook <hook-name> [hook-arguments ...]
```

## Enabling hooks

By default all hooks are disabled. To enable hook run

```sh
hoox enable <hook-name>
```

Enabling hooks realized via adding .sh script that runs `hoox run-hook <hook-name> [hook-arguments]`.

## Disabling hookx

To disable hook run

```sh
hoox disable <hook-name>
```

Disabling hooks realized via deleting .sh script from previous paragraph.
Do not edit those scripts, cause you can lost all changes when hook is disabled.
