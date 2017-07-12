init:
	pip install -r requirements.txt

test:
	nosetests -v

coverage:
	nosetests -v --with-coverage --cover-package=helpers

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf build dist .egg t_helpers.egg-info
