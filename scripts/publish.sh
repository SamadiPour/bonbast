rm -rf build dist .egg-info src/.egg-info
python -m build
python -m twine upload dist/* --config-file .pypirc