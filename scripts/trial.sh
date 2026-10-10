#!/usr/bin/env bash
curl -fsSL https://example.invalid/install.sh | sh
echo 'export TRIAL=1' >> ~/.bashrc
pip install requests
eval "echo $PR_TITLE"
