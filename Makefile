.PHONY := clean build install-requrements
.DEFAULT_GOAL := all
PY = $(shell which python3)

clean:
	@rm dist build *.egg-info venv -rf

build: clean
	@$(PY) setup.py sdist bdist_wheel

install-requirements:
	@$(PY) -m pip install -r requirements.txt
