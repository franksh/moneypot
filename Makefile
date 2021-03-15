PKG=moneypot
PWD=$(shell pwd)

default: 
	make python

clean:
	-rm -f *.o
	make pyclean

clean_all:
	make clean
	make pyclean

pyclean:
	-rm -f *.so
	-rm -rf *.egg-info*
	-rm -rf ./tmp/
	-rm -rf ./build/

python:
	python setup.py develop --user
	# pip install -e ${PWD}

checkdocs:
	python setup.py checkdocs

#pypi:
#	rm dist/*
#	python setup.py sdist
#	twine check dist/*
#
#upload:
#	twine upload dist/*

readme:
	pandoc --from markdown_github --to rst README.md > _README.rst
	sed -e "s/^\:\:/\.\. code\:\: bash/g" _README.rst > README.rst
	rm _README.rst
	rstcheck README.rst

test:
	pytest --cov=${PKG} ${PKG}/tests/

authors:
	python authorlist.py

grootinstall:
	/opt/python36/bin/pip3.6 install --user ../moneypot

groot:
	git fetch
	git pull
	make grootinstall
