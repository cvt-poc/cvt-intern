# Week 2 · Day 1

**Objective:** Create Action: run 'drift-detect render/diff' on pull_request

**Location:** .github/workflows/

**Resource & Why:** GitHub Actions pull_request trigger docs

**LLM Prompt:** Write a GH Action that, on pull_request, checks out the code, installs Helm & kubectl, and runs 'drift-detect render' and 'drift-detect diff'.
