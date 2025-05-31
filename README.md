# Before you run

- This repo has pre-commit to install it follwo these steps.
- Pre-commit uses ruff to reformat the code, and forbids pushing to the main branch. Also it uses mypy a static type checker for Python.
### Add pre-commit
```shell
poetry add pre-commit --dev
```
### Install git hook scripts
```shell
pre-commit install
```
### Run on all files
- It is good practice to run pre-commit to check if everything is set up properly
```shell
pre-commit run --all-files
```

# Github Action 
- This action should pass for you to be able to merge branch with the main