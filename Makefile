install:
	pip install -r requirements.txt

health:
	python health_check.py

clean:
	find . -name "__pycache__" -exec rm -rf {} +
