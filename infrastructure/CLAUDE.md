# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Pulumi-based infrastructure project for an AWS Bedrock playground. The project uses Python with uv for dependency management and creates AWS resources including S3 buckets.

## Development Setup and Commands

### Initial Setup
Before working with this infrastructure:
1. Set AWS profile: `export AWS_PROFILE=...`
2. Login to Pulumi: `pulumi login`
3. Select the correct stack: `pulumi stack select aws-bedrock-playground`
4. Install dependencies: `uv sync`

### Common Commands
- **Preview changes**: `pulumi preview`
- **Deploy infrastructure**: `pulumi up --yes`
- **Destroy infrastructure**: `pulumi destroy`
- **Check stack status**: `pulumi stack ls`

### Architecture

The infrastructure is defined in `__main__.py` and currently provisions:
- S3 bucket for the playground
- Exports the bucket name for reference

The project uses:
- Pulumi for infrastructure as code
- Python 3.13+ runtime with uv toolchain
- AWS provider for resource provisioning

### Important Notes
- Always tear down infrastructure with `pulumi destroy` when done
- The stack name is `aws-bedrock-playground`
- Dependencies are managed through `pyproject.toml` and locked in `uv.lock`