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
- This GitHub action will run once you create a Pull Request. 
- The action will install poetry and pytest, and then it will pass only if all tests pass. 
- This will somewhat minimize the errors in deployment.

### Ruleset 
- No direct commit to main
- Pre-commit reformats, and type checks
- Once PR is created test have to pass for it to be merged
- Additionally, I could add that there has to be 1 approver of the code.
