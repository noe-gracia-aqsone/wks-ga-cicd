# Workshop Exercise: CI/CD Applied to Machine Learning (GitHub Actions + CML + DVC + Hugging Face)

## Goal
Build a practical ML CI/CD pipeline by completing a guided workflow with missing parts.

By the end, participants should be able to:
- Run training automatically in GitHub Actions.
- Pull versioned data with DVC from Hugging Face.
- Publish a CML report as a PR comment.
- (Optional) Deploy artifacts/app to Hugging Face Space.

## Branch Purpose
This `correction` branch contains only the completed reference implementation.

Repository contents used as the reference solution:
- `train.py`
- `Makefile`
- `.github/workflows/ci.yml`
- `.github/workflows/cd.yml`
- `dvc.yaml`
- `data/drug200.csv.dvc`

## Prerequisites
1. Create GitHub repository settings:
   - `Settings > Secrets and variables > Actions`
2. Add the following:
   - Secret: `HF_TOKEN`
   - Variable: `HF_DATASET_URL` with value `https://huggingface.co/datasets/milotix/drug200`
3. Confirm workflow permissions:
   - `Settings > Actions > General > Workflow permissions`
   - Select `Read and write permissions`

## One-Time Configuration (Instructor + Participants)

### 1) Create a Hugging Face token
1. Go to `https://huggingface.co/settings/tokens`
2. Click `New token`
3. Name: `github-actions-cicd-ml`
4. Role:
   - `read` is enough for this workshop data import flow
   - `write` is needed only if you also do Space deployment
5. Copy token value (starts with `hf_...`)

### 2) Add GitHub Actions secrets and variables
In the repository:
- `Settings > Secrets and variables > Actions`
- Add secret:
  - `HF_TOKEN = <your hf_... token>`
- Add variable:
  - `HF_DATASET_URL = https://huggingface.co/datasets/milotix/drug200`

### 3) Initialize DVC and import dataset from Hugging Face
Run once at repository root:

```bash
dvc init
git rm --cached data/drug200.csv
git commit -m "Stop tracking dataset in Git"
dvc import --force https://huggingface.co/datasets/milotix/drug200 drug200.csv -o data/drug200.csv
git add .dvc .dvcignore data/drug200.csv.dvc data/.gitignore
git commit -m "Track dataset with DVC import from Hugging Face"
git push
```

Notes:
- If `dvc init` says `.dvc exists`, skip it.
- In this workshop, Hugging Face is used as an import source (`dvc import`), not as a writable DVC remote.
- Do not run `dvc remote add -d myremote hf://...` for this repo.

### 4) CI-specific notes
- `iterative/setup-cml@v2` should use `vega: false` to avoid `canvas` build failures in GitHub runners.
- Keep Python on a stable version (`3.11` recommended for workshop reproducibility).

## Exercise Steps

### Step 1: Complete workflow environment config
In the exercise branch, complete `.github/workflows/ci.yml` so it includes:
- Python version variable
- Hugging Face dataset variable
- Hugging Face token secret

Expected result:
- Workflow reads values from `vars` and `secrets`, not hardcoded values.

### Step 1b: Complete the Makefile
In the exercise branch, complete `Makefile` so the workflow can call the required targets.

Expected result:
- The workflow can run all required `make` targets without changing the workflow design.

### Step 2: Complete data + training stages
Replace the combined training step with two clear steps:
1. Pull data with DVC (you have the dvc file in `data/`)
2. Reproduce the ML pipeline with DVC

Expected result:
- Logs clearly show data pull and model training as separate stages.

### Step 3: Complete CML reporting stage
Keep the CML report step and ensure it can comment on PRs.

Expected result:
- PR gets a comment containing:
  - Model metrics from `results/metrics.txt`
  - Confusion matrix image link
  - DVC status block

### Step 4 (Optional): Inspect the deployment workflow
Open `.github/workflows/cd.yml` and explain:
- Why deployment is separated from CI
- How `workflow_run` depends on CI success
- Why the same `HF_TOKEN` secret is reused

Expected result:
- Successful CI completion can trigger deployment to Hugging Face Space.

## What To Compare Against
Use this branch as the correction/reference for:
- `.github/workflows/ci.yml`
- `.github/workflows/cd.yml`
- `Makefile`
- `dvc.yaml`

## Validation Checklist
- Workflow triggers on `pull_request` and `push` to `main`.
- No hardcoded secret in YAML.
- `Makefile` contains the commands required by the workflow.
- DVC pull succeeds in CI logs.
- `dvc repro` runs in CI and generates artifacts.
- PR contains CML comment.
- CD uses `HF_TOKEN` consistently.
