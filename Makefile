init:
	pip install -r requirements.txt

publish:
	pip install 'twine>=1.5.0' wheel
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf build dist .egg t_helpers.egg-info
