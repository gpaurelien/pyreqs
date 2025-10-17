format:
	isort pyreqs/
	black pyreqs/

typecheck:
	mypy pyreqs/

lint:
	flake8 pyreqs/
