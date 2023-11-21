.PHONY: all run clean

VENV = venv

ifeq ($(OS),Windows_NT)
	ACTIVATE = $(VENV)/Scripts/activate
	PYTHON = $(VENV)/Scripts/python3
	PIP = $(VENV)/Scripts/pip
	RM = rd /s /q
else
	ACTIVATE = $(VENV)/bin/activate
	PYTHON = $(VENV)/bin/python3
	PIP = $(VENV)/bin/pip
	RM = rm -rf
endif

all: run

run: $(ACTIVATE)
	$(PYTHON) main.py


$(ACTIVATE): requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt


clean:
	$(RM) __pycache__
	$(RM) $(VENV)
