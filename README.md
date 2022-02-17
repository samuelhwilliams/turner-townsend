# Turner & Townsend Backend Assessment

Implementation of the Fifth interpreter from https://github.com/turner-townsend/backend-assessment.

# Run using Docker

To run the Fifth interpreter:

* `make build` (if needed)
* `make run`

To run the test suite:

* `make test`

# Run locally

Instlal the pinned version of Python defined in `.python-version` (probably using pyenv) and then:

* `make run-local`

## TODO: Other good things to add

Static checks such as mypy, pylint.

Auto formatting such as black, isort.

Enforce on CI and potentially via git commit hooks.