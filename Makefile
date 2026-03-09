PYTHON = python3
MAIN = a_maze_ing.py

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

lint:
	flake8 .

lint-strict:
	flake8 .
	mypy . --strict