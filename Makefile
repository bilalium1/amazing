PYTHON = python3
MAIN = a_maze_ing.py
SRCS = maze_gen maze_show main_menu.py $(MAIN)
OUTPUT_FILE = $(shell grep -i "OUTPUT_FILE" config.txt | cut -d'=' -f2)

all: run clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	rm -rf $(OUTPUT_FILE)

lint:
	python3 -m flake8 $(SRCS)
	python3 -m mypy $(SRCS) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

valid:
	python3 output_validator.py $(OUTPUT_FILE)