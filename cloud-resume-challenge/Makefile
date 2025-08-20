# ==============================
# Cloud Resume Challenge - Makefile
# ==============================
# Usage:
#   make build
#   make deploy-infra
#   make deploy-site
#   make invalidate-cdn
#   make deploy-all
#   make seed-db
#   make invoke-put
#   make invoke-get
#   make start-api
#

.PHONY: build deploy-infra deploy-site invalidate-cdn deploy-all seed-db invoke-put invoke-get start-api show-outputs

# -------- Config --------
AWS_VAULT_PROFILE ?= my-user
# S3 bucket must match the name in your SAM template.yaml
BUCKET            ?= joaquin-monque-resume-challenge-website
# Your CloudFront Distribution ID (fill this in once; `aws cloudfront list-distributions` to look it up)
DISTRIBUTION_ID   ?= E2DMPVSG894QSM
# Folder that contains index.html, css, js, assets, etc.
SITE_DIR          ?= ./resume-site

# -------- Build / Deploy Infra --------
build:                  ## Build SAM (packs Lambdas)
	sam build

deploy-infra:           ## Build + Deploy SAM stack (infra + APIs)
	sam build && aws-vault exec $(AWS_VAULT_PROFILE) --no-session -- sam deploy

show-outputs:           ## Print stack outputs (API URLs, etc.)
	aws-vault exec $(AWS_VAULT_PROFILE) --no-session -- aws cloudformation describe-stacks \
	  --stack-name cloud-resume-challenge \
	  --query "Stacks[0].Outputs" --output table

# -------- Frontend (S3 + CloudFront) --------
deploy-site:            ## Sync static site to S3
	aws-vault exec $(AWS_VAULT_PROFILE) --no-session -- aws s3 sync $(SITE_DIR) s3://$(BUCKET) --delete

invalidate-cdn:         ## Invalidate CloudFront cache so updates show immediately
	aws-vault exec $(AWS_VAULT_PROFILE) --no-session -- aws cloudfront create-invalidation \
	  --distribution-id $(DISTRIBUTION_ID) --paths "/*"

deploy-all:             ## One-shot: deploy infra, upload site, invalidate CDN
	$(MAKE) deploy-infra
	$(MAKE) deploy-site
	$(MAKE) invalidate-cdn
	@echo "✅ Deploy complete."

# -------- Local testing (Lambdas / API) --------
invoke-put:             ## Build + invoke PutFunction locally
	sam build && aws-vault exec $(AWS_VAULT_PROFILE) --no-session -- sam local invoke PutFunction

invoke-get:             ## Build + invoke GetFunction locally
	sam build && aws-vault exec $(AWS_VAULT_PROFILE) --no-session -- sam local invoke GetFunction

start-api:              ## Run API Gateway locally on :3000 (good for quick checks)
	aws-vault exec $(AWS_VAULT_PROFILE) --no-session -- sam local start-api

# -------- Utilities --------
seed-db:                 ## Seed DynamoDB with initial visitor_count=0 (run once)
	aws-vault exec $(AWS_VAULT_PROFILE) --no-session -- aws dynamodb put-item \
	  --table-name cloud-resume-challenge \
	  --item '{"ID":{"S":"visitor_count"},"count":{"N":"0"}}' \
	  || true
