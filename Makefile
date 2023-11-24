.PHONY: all run clean

VENV = venv

ifeq ($(OS),Windows_NT)
	PYTHON = python
	ACTIVATE = $(VENV)/Scripts/activate
	PYTHON_VENV = $(VENV)/Scripts/python
	PIP = $(VENV)/Scripts/pip
	RM = rd /s /q
else
	PYTHON = python3
	ACTIVATE = $(VENV)/bin/activate
	PYTHON_VENV = $(VENV)/bin/python3
	PIP = $(VENV)/bin/pip
	RM = rm -rf
endif

all: run

run: $(ACTIVATE)
	$(PYTHON_VENV) main.py


$(ACTIVATE): requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt


clean:
	$(RM) __pycache__
	$(RM) $(VENV)
