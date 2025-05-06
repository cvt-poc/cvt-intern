#!/bin/bash
# CVT-Intern Program: GitHub Organization Setup Script
# This script automates the creation of repositories and project structure for the internship program
# Prerequisites: GitHub CLI (gh) installed and authenticated

# Configuration
ORG_NAME="cvt-poc"
PROJECTS=("drift-detect" "k8s-autoscaler-advisor" "secrets-lifecycle" "helm-score" "chaos-injector" "cost-tagger" "infra-graph" "alert-consolidator" "canary-configurator" "release-notes-compiler")
PROJECT_DESCRIPTIONS=(
  "A GitHub Action that compares live cluster state against Helm templates, preventing configuration drift"
  "A CLI tool that analyzes HPA/VPA configurations and recommends optimal targets"
  "A CLI and GitHub Action that automates Kubernetes Secrets rotation via AWS Secrets Manager"
  "A REST service wrapping helm lint and kubeval, scoring charts on security and best practices"
  "A wrapper around Chaos Engineering tools offering a unified CLI to trigger various experiments"
  "A Terraform pre-commit hook that enforces and auto-inserts cost allocation tags"
  "A dashboard that visualizes service-to-service call graphs in Kubernetes using eBPF"
  "A Prometheus sidecar that de-duplicates alerts with identical labels"
  "A CLI that converts a Helm chart into a Canary rollout YAML with sensible defaults"
  "A GitHub Action that aggregates merged PR titles and authors into formatted release notes"
)

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo "" >> README.md
    
    # Create CONTRIBUTING.md
    echo "# Contributing to $PROJECT" > CONTRIBUTING.md
    echo "" >> CONTRIBUTING.md
    echo "Thank you for your interest in contributing to this project!" >> CONTRIBUTING.md
    echo "" >> CONTRIBUTING.md
    echo "## Pull Request Process" >> CONTRIBUTING.md
    echo "" >> CONTRIBUTING.md
    echo "## Code Style Guidelines" >> CONTRIBUTING.md
    echo "" >> CONTRIBUTING.md
    echo "## Testing Requirements" >> CONTRIBUTING.md
    
    # Create ONBOARDING.md
    echo "# Onboarding Guide for $PROJECT" > ONBOARDING.md
    echo "" >> ONBOARDING.md
    echo "Welcome to the $PROJECT internship! This guide will help you get started." >> ONBOARDING.md
    echo "" >> ONBOARDING.md
    echo "## First-Day Checklist" >> ONBOARDING.md
    echo "" >> ONBOARDING.md
    echo "## Development Environment" >> ONBOARDING.md
    echo "" >> ONBOARDING.md
    echo "## Project Structure" >> ONBOARDING.md
    
    # Create issue templates
    mkdir -p .github/ISSUE_TEMPLATE
    
    # Task issue template
    cat > .github/ISSUE_TEMPLATE/task.md << 'EOL'
---
name: Task
about: A specific implementation task
title: "[TASK]: "
labels: task
assignees: ''
---

## Description
<!-- Describe the task in detail -->

## Acceptance Criteria
<!-- List specific criteria that must be met for this task to be complete -->

## Technical Notes
<!-- Any technical guidance or references that might help -->

## Time Estimate
<!-- Estimated time to complete this task -->
EOL
    
    # Learning Checkpoint template
    cat > .github/ISSUE_TEMPLATE/learning-checkpoint.md << 'EOL'
---
name: Learning Checkpoint
about: Verify knowledge acquisition milestone
title: "[LEARNING]: "
labels: learning
assignees: ''
---

## Learning Objectives
<!-- List specific knowledge or skills to be demonstrated -->

## Verification Method
<!-- How will this knowledge be demonstrated? -->

## Resources
<!-- Helpful resources for this learning checkpoint -->
EOL
    
    # Blocker template
    cat > .github/ISSUE_TEMPLATE/blocker.md << 'EOL'
---
name: Blocker
about: Report a technical or conceptual roadblock
title: "[BLOCKER]: "
labels: blocker, help-wanted
assignees: ''
---

## Description
<!-- Describe what's blocking your progress -->

## What I've Tried
<!-- List approaches you've already attempted -->

## Specific Questions
<!-- What specific questions do you need answers to? -->

## Relevant Code/Logs
<!-- Include any relevant code snippets or error messages -->
EOL
    
    # Weekly Reflection template
    cat > .github/ISSUE_TEMPLATE/weekly-reflection.md << 'EOL'
---
name: Weekly Reflection
about: Document weekly learning and progress
title: "Week [NUMBER] Reflection"
labels: reflection
assignees: ''
---

## What I Accomplished
<!-- List your key accomplishments this week -->

## What I Learned
<!-- Describe new concepts, technologies, or techniques you learned -->

## Challenges Faced
<!-- Discuss challenges and how you addressed them -->

## Next Week's Goals
<!-- What do you plan to accomplish next week? -->

## Questions/Clarifications Needed
<!-- Any questions you need answered? -->
EOL
    
    # Create GitHub workflow for issue tracking
    mkdir -p .github/workflows
    
    cat > .github/workflows/issue-tracker.yml << 'EOL'
name: Issue Tracker

on:
  issues:
    types: [opened, closed, reopened, assigned, unassigned]
  pull_request:
    types: [opened, closed, reopened]

jobs:
  update-project-board:
    runs-on: ubuntu-latest
    steps:
      - name: Update Project Board
        uses: actions/github-script@v6
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            console.log('Issue or PR activity detected, would update project board');
            // Project automation will be configured via GitHub's UI
EOL
    
    # Create workflow for activity tracking
    cat > .github/workflows/activity-tracker.yml << 'EOL'
name: Activity Tracker

on:
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight

jobs:
  track-activity:
    runs-on: ubuntu-latest
    steps:
      - name: Check Recent Activity
        uses: actions/github-script@v6
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            console.log('Checking for recent intern activity');
            // This would track activity and notify mentors of inactivity
EOL
    
    # Commit and push changes
    git add .
    git commit -m "Initial repository structure setup"
    git push
    
    echo -e "${GREEN}Repository $PROJECT has been set up successfully.${NC}"
    
    # Return to parent directory
    cd ..
done

echo -e "\n${GREEN}=== Setup Complete ===${NC}"
echo "All repositories have been created and initialized with the basic structure."
echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Populate Week 1 content for each project"
echo "2. Configure GitHub Project boards for each repository"
echo "3. Set up branch protection rules"
echo "4. Invite interns and assign them to projects" -e "${BLUE}=== CVT-Intern Program: GitHub Organization Setup ===${NC}"
echo "This script will set up the GitHub organization and repositories."

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI (gh) is not installed or not in PATH.${NC}"
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}You are not authenticated with GitHub CLI.${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

# Create organization if it doesn't exist
echo -e "\n${YELLOW}Checking if organization exists...${NC}"
if ! gh api orgs/$ORG_NAME &> /dev/null; then
    echo -e "${YELLOW}Creating organization: $ORG_NAME${NC}"
    # Note: GitHub CLI doesn't directly support org creation, this would need to be done manually
    echo -e "${RED}Please create the organization manually at https://github.com/organizations/new${NC}"
    echo "Then press Enter to continue..."
    read
else
    echo -e "${GREEN}Organization $ORG_NAME already exists.${NC}"
fi

# Create project board templates
echo -e "\n${YELLOW}Creating organization-wide project templates...${NC}"

# Create repositories for each project
for i in "${!PROJECTS[@]}"; do
    PROJECT=${PROJECTS[$i]}
    DESCRIPTION=${PROJECT_DESCRIPTIONS[$i]}
    
    echo -e "\n${YELLOW}Setting up repository: $PROJECT${NC}"
    
    # Check if repo exists
    if gh repo view $ORG_NAME/$PROJECT &> /dev/null; then
        echo -e "${GREEN}Repository $ORG_NAME/$PROJECT already exists.${NC}"
    else
        echo "Creating repository: $PROJECT"
        gh repo create $ORG_NAME/$PROJECT --public --description "$DESCRIPTION"
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create repository $PROJECT. Skipping.${NC}"
            continue
        fi
    fi
    
    # Clone the repository
    echo "Cloning repository: $PROJECT"
    if [ -d "$PROJECT" ]; then
        echo -e "${YELLOW}Directory $PROJECT already exists. Pulling latest changes.${NC}"
        cd $PROJECT
        git pull
        cd ..
    else
        gh repo clone $ORG_NAME/$PROJECT
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to clone repository $PROJECT. Skipping.${NC}"
            continue
        fi
    fi
    
    # Create directory structure
    cd $PROJECT
    echo "Creating directory structure for $PROJECT..."
    
    mkdir -p setup resources/{sample_configs,cheat_sheets,case_studies,architecture} weekly_tasks
    
    # Create initial weeks structure
    for week in {1..24}; do
        mkdir -p weekly_tasks/week-$week
        
        # Create README for each week
        echo "# Week $week Overview" > weekly_tasks/week-$week/README.md
        echo "" >> weekly_tasks/week-$week/README.md
        echo "## Learning Objectives" >> weekly_tasks/week-$week/README.md
        echo "" >> weekly_tasks/week-$week/README.md
        echo "## Daily Tasks" >> weekly_tasks/week-$week/README.md
        
        # Create files for each day in the week
        for day in {1..5}; do
            echo "# Week $week Day $day: [Title]" > weekly_tasks/week-$week/day-$day.md
            echo "" >> weekly_tasks/week-$week/day-$day.md
            echo "## Overview" >> weekly_tasks/week-$week/day-$day.md
            echo "- **Duration**: Full day (8 hours)" >> weekly_tasks/week-$week/day-$day.md
            echo "- **Why This Matters**: [Explanation]" >> weekly_tasks/week-$week/day-$day.md
            echo "- **Connection to Project**: [Explanation]" >> weekly_tasks/week-$week/day-$day.md
            echo "" >> weekly_tasks/week-$week/day-$day.md
            echo "## Morning Session (4 hours)" >> weekly_tasks/week-$week/day-$day.md
            echo "" >> weekly_tasks/week-$week/day-$day.md
            echo "## Afternoon Session (4 hours)" >> weekly_tasks/week-$week/day-$day.md
        done
    done
    
    # Create setup scripts
    echo "#!/bin/bash" > setup/setup.sh
    echo "# Setup script for $PROJECT" >> setup/setup.sh
    echo "echo \"Setting up development environment for $PROJECT...\"" >> setup/setup.sh
    chmod +x setup/setup.sh
    
    # Create PowerShell setup script for Windows users
    echo "# Setup script for $PROJECT" > setup/setup.ps1
    echo "Write-Host \"Setting up development environment for $PROJECT...\"" >> setup/setup.ps1
    
    # Create validation script
    echo "#!/bin/bash" > setup/validate.sh
    echo "# Validation script for $PROJECT" >> setup/validate.sh
    echo "echo \"Validating development environment for $PROJECT...\"" >> setup/validate.sh
    chmod +x setup/validate.sh
    
    # Create README
    echo "# $PROJECT" > README.md
    echo "" >> README.md
    echo "$DESCRIPTION" >> README.md
    echo "" >> README.md
    echo "## Project Overview" >> README.md
    echo "" >> README.md
    echo "## Getting Started" >> README.md
    echo "" >> README.md
    echo "### Prerequisites" >> README.md
    echo "" >> README.md
    echo "### Setup" >> README.md
    echo