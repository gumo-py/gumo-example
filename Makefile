pip_compile_option = --upgrade-package gumo-core --upgrade-package gumo-datastore --upgrade-package gumo-task --upgrade-package gumo-task-emulator

.PHONY: setup
setup:
	[ -d venv ] || python3 -m venv venv
	pip3 install twine wheel pytest

.PHONY: pip-compile
pip-compile:
	cd server; \
	pip install --upgrade gumo-core gumo-datastore gumo-task gumo-task-emulator; \
	pip-compile ${pip_compile_option} --output-file src/requirements.txt src/requirements.in ; \
	pip-compile ${pip_compile_option} --output-file test/requirements.testing.txt test/requirements.testing.in src/requirements.txt
