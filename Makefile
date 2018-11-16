ACTIVATE_VENV = . venv/bin/activate

.PHONY:
	activate-venv \
	install-req \
	setup \
	show \
	virt-env \
	destroy \
	flake8 \

setup: destroy virt-env; . venv/bin/activate

test: setup activate-venv; pytest tests/test.py

activate-venv:
	. venv/bin/activate

destroy:
	if [ -d venv/ ]; then rm -rf venv/; fi

install-req:
	pip install -r requirements.txt

virt-env:
	python3 -m venv venv

flake8:
	flake8 --exclude venv
