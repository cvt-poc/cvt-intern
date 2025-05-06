# Drift-Detect Intern Project

**Drift-Detect** is a hands-on, 24-week internship project where you’ll build a production-grade drift-detection toolchain from the ground up. By the end of this journey, you’ll have delivered a feature-complete CLI, REST API, observability dashboards, alerting integrations, and packaging modules—plus marketable collateral and real-world SRE/DevOps skills.

---

## 🎯 Project Goals

1. **Enforce Git→Cluster Fidelity**  
   Build a system that renders Helm charts, diffs them against live Kubernetes clusters, and reports configuration drift automatically on pull requests.

2. **Deliver Tier-3 “Full Stack” Tooling**  
   - **CLI** (Typer) with `render` & `diff` commands  
   - **API** (FastAPI) exposing `/render-diff`, `/report`, `/events`  
   - **Dashboard** (Grafana + Prometheus + Alertmanager + Slack)  
   - **Packaging** (Helm chart, Terraform module, CI/CD pipelines, security scans, runbook)

3. **Generate Demos & Case Study Assets**  
   Weekly demos, dashboards screenshots, blog outlines, and a final walkthrough video.

---

## 📚 Intern Learning Experience

Over 120 detailed day-by-day guides you will:

- Master **Git**, **Docker**, **Kind**, **Helm**, **Terraform**, **Python** (Typer, FastAPI, Pydantic, SQLModel)  
- Build robust **CI/CD pipelines** in **GitHub Actions**  
- Design and automate **observability** with **Prometheus**, **Grafana**, and **Alertmanager**  
- Package infrastructure with **Helm charts** and **Terraform modules**  
- Enforce security with **Trivy** & **tfsec** scans  
- Document and demo your work via **runbooks**, **demo videos**, and **blog outlines**

Each day’s guide lives under `projects/drift-detect/foundation/week-<n>/day-<d>.md`, with clear objectives, resource links, and an “LLM Prompt” to accelerate learning.

---

## 🏗️ Project Structure

```text
projects/drift-detect/
├── cli/             # Typer CLI code & pytest suite
├── api/             # FastAPI service & HTTPX tests
├── controller/      # (Future extension for custom controllers)
├── dashboard/       # Grafana JSON, PrometheusRules, Alertmanager configs
├── infra/           # Helm chart & Terraform module
├── ci/              # GitHub Actions workflows
├── docs/            # runbook.md, API spec, demo artifacts
└── foundation/      # week-0 … week-23/day-1 … day-5 markdown guides
