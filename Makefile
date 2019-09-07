all: isort yapf flake8 pytest
test: pytest

isort:
	isort -y -rc .

yapf:
	yapf -i -r .

flake8:
	flake8 .

pytest:
	PYTHONPATH=app:. pytest
