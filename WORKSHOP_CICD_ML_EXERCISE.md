# Workshop Exercise: CI/CD Applied to Machine Learning (GitHub Actions + CML + DVC + Hugging Face)

## Goal
Build a practical ML CI/CD pipeline by completing a guided workflow with missing parts.

By the end, participants should be able to:
- Run training automatically in GitHub Actions.
- Pull versioned data with DVC from Hugging Face.
- Publish a CML report as a PR comment.
- (Optional) Deploy artifacts/app to Hugging Face Space.

## Starting Point
- Repository already contains:
  - `train.py`
  - `Makefile` with ML/CML/DVC helpers
  - `.github/workflows/ci.yml` with TODO gaps
  - `data/drug200.csv.dvc` imported from Hugging Face dataset

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
Open `.github/workflows/ci.yml` and complete TODOs for:
- Python version variable
- Hugging Face dataset variable
- Hugging Face token secret

Expected result:
- Workflow reads values from `vars` and `secrets`, not hardcoded values.

### Step 2: Complete data + training stages
Replace the combined training step with two clear steps:
1. Pull data with DVC
2. Train the model

Expected result:
- Logs clearly show data pull and model training as separate stages.

### Step 3: Complete CML reporting stage
Keep the CML report step and ensure it can comment on PRs.

Expected result:
- PR gets a comment containing:
  - Model metrics from `results/metrics.txt`
  - Confusion matrix image link
  - DVC status block

### Step 4 (Optional): Add deploy job
Create a `deploy-space` job:
- Needs training job completion
- Runs only on `push` to `main`
- Uses `make deploy HF=${{ secrets.HF_TOKEN }}`

Expected result:
- Successful main branch push updates Hugging Face Space content.

## Validation Checklist
- Workflow triggers on `pull_request` and `push` to `main`.
- No hardcoded secret in YAML.
- DVC pull succeeds in CI logs.
- `train.py` runs in CI and generates artifacts.
- PR contains CML comment.
- Optional deploy job runs only for `main` push.
