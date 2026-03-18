# Install Python dependencies used by training, evaluation, and deployment.
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# Auto-format Python files in the repository root.
format:
	black *.py
