# Glossary

## Authority
The human-readable Markdown file (`docs/authorised-skill-repositories.md`) that defines which skill repositories are allowed to be used or updated. This is the single source of truth for repository allowlists.

## Projection
The machine-readable JSON file (e.g., `golden-skills.json`) derived from the Authority. It must not be manually edited to bypass the Authority.

## Syafiq's Skills Repository
This repository (`syafiq-kay-skills`), containing Syafiq's custom agent skills, onboarding routines, and automated workflows.

## Authorised Skill Repository
A third-party or external repository (like `mattpocock-skills` or `basic-memory-skills`) that has been explicitly permitted in the Authority.

## Skills CLI
The future command-line interface to manage, verify, update, and heal agent skills.
