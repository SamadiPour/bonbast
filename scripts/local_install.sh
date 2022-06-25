rm -rf build dist .egg-info src/.egg-info
python -m build
yes | python -m pip uninstall bonbast
python -m pip install dist/*.whl
