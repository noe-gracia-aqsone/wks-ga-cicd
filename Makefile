install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py

train:
	python train.py

eval:
	echo "## Model Metrics" > report.md
	cat ./results/metrics.txt >> report.md
		
	echo "\n## Confusion Matrix Plot" >> report.md
	echo '![Confusion Matrix](./results/model_results.png)' >> report.md
	
	cml comment create report.md

update-branch:
	git config --global user.name $(USER_NAME)
	git config --global user.email $(USER_EMAIL)
	git commit -am "Update with new results"
	git push --force origin HEAD:update

hf-login:
	# Install the latest version with CLI support
	pip install -U "huggingface_hub[cli]"
	# Use the new 'hf' binary for authentication
	hf auth login --token $(HF) --add-to-git-credential

push-hub:
	# Use the new 'hf upload' syntax
	hf upload milotix/DrugClassification ./app . --repo-type=space --commit-message="Sync App files"
	hf upload milotix/DrugClassification ./model /model --repo-type=space --commit-message="Sync Model"
	hf upload milotix/DrugClassification ./results /metrics --repo-type=space --commit-message="Sync Metrics"
	
deploy: hf-login push-hub