.PHONY: all run clean

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

all: run

run: $(VENV)/bin/activate
	$(PYTHON) main.py


$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
 	$(PIP) install -r requirements.txt


clean:
	rm -rf __pycache__
	rm -rf $(VENV)
