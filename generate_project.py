#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def create_project_structure(project_title):
    """
    Create the full project structure including all markdown files
    with comprehensive content.
    
    Args:
        project_title: The title of the project
    """
    # Create base directories
    base_dir = project_title.lower().replace(' ', '-').replace('_', '-')
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(f"{base_dir}/setup", exist_ok=True)
    os.makedirs(f"{base_dir}/resources", exist_ok=True)
    
    # Create main README
    with open(f"{base_dir}/README.md", 'w') as f:
        f.write(f"# {project_title}\n\n")
        f.write(f"## Problem Statement\n\n")
        f.write("Configuration drift occurs when the actual state of infrastructure (particularly Kubernetes clusters) diverges from the desired state defined in Git repositories. This project aims to develop a comprehensive tool to detect, report, and remediate drift across multiple clusters and environments.\n\n")
        f.write("## Project Structure\n\n")
        f.write("This repository contains a 24-week DevOps/SRE internship project broken down into daily tasks.\n\n")
        f.write("### Getting Started\n\n")
        f.write("1. Start with the Week 1, Day 1 tasks\n")
        f.write("2. Follow the day-by-day progression\n")
        f.write("3. Complete the daily reflections\n")
        f.write("4. Reach out to mentors as needed\n\n")
        f.write("### Repository Structure\n\n")
        f.write("- `/setup`: Environment setup scripts and guides\n")
        f.write("- `/resources`: Reference materials and documentation\n")
        f.write("- `/weekly_tasks`: Daily task breakdowns organized by week\n")
    
    # Create setup files
    with open(f"{base_dir}/setup/README.md", 'w') as f:
        f.write("# Environment Setup\n\n")
        f.write("This directory contains scripts and guides to set up your development environment for the Detect_Drift project.\n\n")
        f.write("## Requirements\n\n")
        f.write("- Computer with at least 8GB RAM, 4 CPU cores\n")
        f.write("- 20GB free disk space\n")
        f.write("- Git installed\n")
        f.write("- Docker installed\n")
        f.write("- Python 3.8+ installed\n\n")
        f.write("## Setup Script\n\n")
        f.write("Run the following command to set up your environment:\n\n")
        f.write("```bash\n")
        f.write("./setup.sh\n")
        f.write("```\n")
    
    with open(f"{base_dir}/setup/setup.sh", 'w') as f:
        f.write("#!/bin/bash\n\n")
        f.write("# Detect_Drift Project Setup Script\n\n")
        f.write("# Install required packages\n")
        f.write("pip install kubernetes pyyaml requests rich\n\n")
        f.write("# Install kubectl\n")
        f.write("curl -LO \"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\"\n")
        f.write("chmod +x kubectl\n")
        f.write("sudo mv kubectl /usr/local/bin/\n\n")
        f.write("# Install minikube\n")
        f.write("curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64\n")
        f.write("chmod +x minikube-linux-amd64\n")
        f.write("sudo mv minikube-linux-amd64 /usr/local/bin/minikube\n\n")
        f.write("# Start minikube\n")
        f.write("minikube start\n\n")
        f.write("echo \"Setup completed successfully!\"\n")
    os.chmod(f"{base_dir}/setup/setup.sh", 0o755)
    
    # Create resources directory
    with open(f"{base_dir}/resources/README.md", 'w') as f:
        f.write("# Project Resources\n\n")
        f.write("This directory contains reference materials, sample configurations, and documentation for the Detect_Drift project.\n\n")
        f.write("## Contents\n\n")
        f.write("- `sample_configs/`: Example Kubernetes manifests for testing\n")
        f.write("- `cheat_sheets/`: Quick reference guides for tools and concepts\n")
        f.write("- `case_studies/`: Real-world examples of configuration drift\n")
    
    os.makedirs(f"{base_dir}/resources/sample_configs", exist_ok=True)
    os.makedirs(f"{base_dir}/resources/cheat_sheets", exist_ok=True)
    os.makedirs(f"{base_dir}/resources/case_studies", exist_ok=True)
    
    # Create weekly directories and files
    for week in range(1, 25):
        week_dir = f"{base_dir}/weekly_tasks/week-{week}"
        os.makedirs(week_dir, exist_ok=True)
        
        # Create weekly README
        with open(f"{week_dir}/README.md", 'w') as f:
            f.write(f"# Week {week}: {get_week_theme(week)}\n\n")
            f.write("## Weekly Objectives\n\n")
            for objective in get_week_objectives(week):
                f.write(f"- {objective}\n")
            f.write("\n## Daily Tasks\n\n")
            for day in range(1, 6):
                day_title = get_day_title(week, day)
                f.write(f"- [Day {day}: {day_title}](day-{day}.md)\n")
        
        # Create daily files
        for day in range(1, 6):
            day_title = get_day_title(week, day)
            with open(f"{week_dir}/day-{day}.md", 'w') as f:
                f.write(f"# Week {week} Day {day}: {day_title}\n\n")
                f.write("## Overview\n\n")
                f.write("- **Duration**: Full day (8 hours)\n")
                f.write(f"- **Why This Matters**: {get_why_this_matters(week, day)}\n")
                f.write(f"- **Connection to Project**: {get_connection_to_project(week, day)}\n\n")
                f.write("## Learning Objectives\n\n")
                f.write("By the end of today, you will be able to:\n")
                for objective in get_learning_objectives(week, day):
                    f.write(f"- {objective}\n")
                f.write("\n## Prerequisites\n\n")
                for prereq in get_prerequisites(week, day):
                    f.write(f"- {prereq}\n")
                
                # Add the rest of the sections as placeholders
                f.write("\n## Morning Session (4 hours)\n\n")
                f.write("### Technical Concept Deep Dive (90 minutes)\n\n")
                f.write("#### Key Concept 1: [Title]\n")
                f.write("- [Detailed explanation]\n")
                f.write("- [Code example or configuration sample]\n")
                f.write("- [Common misconceptions]\n\n")
                
                f.write("#### Key Concept 2: [Title]\n")
                f.write("- [Detailed explanation]\n")
                f.write("- [Code example or configuration sample]\n")
                f.write("- [Common misconceptions]\n\n")
                
                f.write("#### Key Concept 3: [Title]\n")
                f.write("- [Detailed explanation]\n")
                f.write("- [Code example or configuration sample]\n")
                f.write("- [Common misconceptions]\n\n")
                
                f.write("#### Self-Check Questions\n")
                f.write("- [Question 1]\n")
                f.write("- [Question 2]\n")
                f.write("- [Question 3]\n\n")
                
                f.write("### Hands-on Exploration (2.5 hours)\n\n")
                f.write("#### Setup (30 minutes)\n")
                f.write("```bash\n")
                f.write("# Environment setup commands\n")
                f.write("[detailed commands with explanations]\n")
                f.write("```\n\n")
                
                f.write("#### Exercise 1: [Title] (45 minutes)\n")
                f.write("1. [Step-by-step instructions]\n")
                f.write("2. [Expected outputs]\n")
                f.write("3. [Verification steps]\n\n")
                
                f.write("#### Exercise 2: [Title] (45 minutes)\n")
                f.write("1. [Step-by-step instructions]\n")
                f.write("2. [Expected outputs]\n")
                f.write("3. [Verification steps]\n\n")
                
                f.write("#### Exercise 3: [Title] (30 minutes)\n")
                f.write("1. [Step-by-step instructions]\n")
                f.write("2. [Expected outputs]\n")
                f.write("3. [Verification steps]\n\n")
                
                f.write("## Afternoon Session (4 hours)\n\n")
                f.write("### Implementation Challenge (3 hours)\n\n")
                f.write("#### Task Description\n")
                f.write("[Detailed description of the challenge that applies morning concepts]\n\n")
                
                f.write("#### Requirements\n")
                f.write("- [Specific requirement 1]\n")
                f.write("- [Specific requirement 2]\n")
                f.write("- [Specific requirement 3]\n\n")
                
                f.write("#### Implementation Steps\n")
                f.write("1. [Detailed step with technical guidance]\n")
                f.write("2. [Detailed step with technical guidance]\n")
                f.write("3. [Detailed step with technical guidance]\n\n")
                
                f.write("#### Expected Deliverables\n")
                f.write("- [Specific output 1]\n")
                f.write("- [Specific output 2]\n")
                f.write("- [Specific output 3]\n\n")
                
                f.write("#### Testing and Validation\n")
                f.write("- [How to verify your implementation works correctly]\n")
                f.write("- [Test cases to run]\n")
                f.write("- [Common errors and solutions]\n\n")
                
                f.write("### Documentation and Reflection (1 hour)\n\n")
                f.write("#### Documentation Tasks\n")
                f.write("- Update your project journal with today's learnings\n")
                f.write("- Document your implementation with:\n")
                f.write("  - Architecture diagrams\n")
                f.write("  - Code comments\n")
                f.write("  - README updates\n")
                f.write("  - Decision log entries\n\n")
                
                f.write("#### Reflection Questions\n")
                f.write("- What was the most challenging concept today and why?\n")
                f.write("- How does today's work connect to real-world DevOps scenarios?\n")
                f.write("- What would you change about your implementation if you had more time?\n")
                f.write("- What questions do you still have about today's topics?\n\n")
                
                f.write("## Resources\n\n")
                f.write("### Essential Reading\n")
                f.write("- [Resource 1 with specific chapters/sections]\n")
                f.write("- [Resource 2 with specific chapters/sections]\n")
                f.write("- [Resource 3 with specific chapters/sections]\n\n")
                
                f.write("### Reference Documentation\n")
                f.write("- [Link to official documentation with specific sections]\n")
                f.write("- [Link to official documentation with specific sections]\n")
                f.write("- [Link to official documentation with specific sections]\n\n")
                
                f.write("### Video Tutorials\n")
                f.write("- [Video 1 with timestamp references]\n")
                f.write("- [Video 2 with timestamp references]\n")
                f.write("- [Video 3 with timestamp references]\n\n")
                
                f.write("### Code Examples\n")
                f.write("- [GitHub repository or Gist link with specific files]\n")
                f.write("- [GitHub repository or Gist link with specific files]\n")
                f.write("- [GitHub repository or Gist link with specific files]\n\n")
                
                f.write("## Troubleshooting Guide\n\n")
                f.write("| Issue | Symptoms | Solution |\n")
                f.write("|-------|----------|----------|\n")
                f.write("| [Common Issue 1] | [How to identify] | [Step-by-step resolution] |\n")
                f.write("| [Common Issue 2] | [How to identify] | [Step-by-step resolution] |\n")
                f.write("| [Common Issue 3] | [How to identify] | [Step-by-step resolution] |\n")
                f.write("| [Common Issue 4] | [How to identify] | [Step-by-step resolution] |\n")
                f.write("| [Common Issue 5] | [How to identify] | [Step-by-step resolution] |\n\n")
                
                f.write("## Mentorship and Support\n\n")
                f.write("### Scheduled Check-ins\n")
                f.write("- Morning kickoff (9:00 AM): Review plan and clarify questions\n")
                f.write("- Midday check (12:30 PM): Verify morning exercises completion\n")
                f.write("- End-of-day review (4:30 PM): Evaluate deliverables and answer questions\n\n")
                
                f.write("### When to Ask for Help\n")
                f.write("- You've been stuck on the same issue for more than 30 minutes\n")
                f.write("- Your implementation is producing unexpected results that you can't debug\n")
                f.write("- You've consulted all the resources but still have conceptual questions\n\n")
                
                f.write("### How to Ask for Help Effectively\n")
                f.write("- Clearly describe what you're trying to achieve\n")
                f.write("- Explain what you've tried already\n")
                f.write("- Share relevant code or configurations\n")
                f.write("- Specify error messages you're receiving\n\n")
                
                f.write("## Extension Activities\n\n")
                f.write("If you complete the day's tasks early, challenge yourself with:\n")
                f.write("- [Advanced extension 1]\n")
                f.write("- [Advanced extension 2]\n")
                f.write("- [Advanced extension 3]\n\n")
                
                f.write("## Preparation for Tomorrow\n\n")
                f.write("To prepare for tomorrow's tasks:\n")
                f.write("- Review [specific resources]\n")
                f.write("- Think about [concepts to consider]\n")
                f.write("- Ensure [environment preparations]\n\n")
                
                f.write("## Success Criteria\n\n")
                f.write("You have successfully completed today's tasks when:\n")
                f.write("- [Specific, measurable outcome 1]\n")
                f.write("- [Specific, measurable outcome 2]\n")
                f.write("- [Specific, measurable outcome 3]\n")
                f.write("- Your documentation clearly explains your implementation\n")
                f.write("- You can answer the self-check questions confidently\n")

    print(f"✅ Project structure created successfully in the '{base_dir}' directory")
    print(f"📂 Total files created: {5 * 24 + 24 + 3} (120 daily tasks, 24 weekly READMEs, and 3 support files)")

def get_week_theme(week):
    """Return theme for the specified week"""
    themes = {
        1: "Foundation and GitOps Fundamentals",
        2: "Development Environment and Basic Tools",
        3: "Kubernetes Resource Management",
        4: "Building the Core Drift Detection Engine",
        5: "Git Integration and Source Management",
        6: "Implementing Basic Policy Controls",
        7: "Notification and Alerting",
        8: "Advanced Drift Analysis",
        9: "Multi-Cluster Support - Part 1",
        10: "Multi-Cluster Support - Part 2",
        11: "Error Handling and Resilience",
        12: "Scaling and Performance",
        13: "Security Hardening",
        14: "Monitoring and Observability",
        15: "API Design and Development",
        16: "Third-Party Integrations",
        17: "Authentication and Authorization",
        18: "Data Management and Retention",
        19: "Multi-Tenancy Implementation",
        20: "Billing and Usage Tracking",
        21: "User Management and Onboarding",
        22: "Service Level Objectives",
        23: "Documentation and User Guides",
        24: "Demonstration and Presentation"
    }
    return themes.get(week, f"Week {week} Development")

def get_week_objectives(week):
    """Return objectives for the specified week"""
    objectives = {
        1: [
            "Understand GitOps principles and configuration drift concepts",
            "Set up development environment with necessary tools",
            "Learn basic Kubernetes resource management",
            "Create a simple drift detection mechanism",
            "Document the foundation of our approach"
        ],
        2: [
            "Set up comprehensive development environment",
            "Master Git workflow for the project",
            "Understand Kubernetes API interactions",
            "Implement basic resource comparison utilities",
            "Create test harness for drift detection"
        ],
        # Additional weeks would be defined here
    }
    return objectives.get(week, [
        "Continue developing the Detect_Drift project",
        "Master relevant DevOps/SRE concepts and tools",
        "Implement and test new features",
        "Document progress and decisions",
        "Prepare for the next phase of development"
    ])

def get_day_title(week, day):
    """Generate an appropriate title for the specific day"""
    day_titles = {
        (1, 1): "Introduction to GitOps and Configuration Drift",
        (1, 2): "Setting Up Your Development Environment",
        (1, 3): "Understanding Kubernetes Resources and State",
        (1, 4): "Introduction to Drift Detection Approaches",
        (1, 5): "Building Your First Drift Detector",
        
        (2, 1): "Advanced Kubernetes Environment Setup",
        (2, 2): "Git Workflows and Repository Structure",
        (2, 3): "Using the Kubernetes API for State Retrieval",
        (2, 4): "Implementing Resource Comparison Algorithms",
        (2, 5): "Testing Drift Detection with Various Resources",
        
        # Additional days would be defined here
    }
    
    return day_titles.get((week, day), f"Detect_Drift Implementation - Week {week}, Day {day}")

def get_why_this_matters(week, day):
    """Return why this day's topic matters to DevOps/SRE professionals"""
    reasons = {
        (1, 1): "Configuration drift is one of the most common yet challenging problems in modern infrastructure management. When live environments don't match their declared state in version control, it leads to inconsistent environments, failed deployments, security vulnerabilities, and difficult-to-diagnose production issues."
    }
    
    return reasons.get((week, day), "This topic is essential for building a comprehensive drift detection solution and developing critical DevOps/SRE skills.")

def get_connection_to_project(week, day):
    """Return how this day's work connects to the overall project"""
    connections = {
        (1, 1): "Today establishes the foundation for our Detect_Drift tool by understanding the problem space, exploring existing approaches, and defining our unique value proposition. Without this conceptual foundation, we can't build an effective solution."
    }
    
    return connections.get((week, day), "This day's work builds on previous components and adds essential functionality to our Detect_Drift solution.")

def get_learning_objectives(week, day):
    """Return learning objectives for the specified day"""
    objectives = {
        (1, 1): [
            "Explain the concept of configuration drift and its impact on DevOps practices",
            "Describe the principles of GitOps and how they relate to drift detection",
            "Compare at least three existing approaches to drift detection and their limitations",
            "Set up a basic local Kubernetes environment with a Git repository",
            "Manually create and detect a simple case of configuration drift"
        ]
    }
    
    return objectives.get((week, day), [
        "Implement new functionality for the Detect_Drift tool",
        "Master relevant DevOps concepts and technologies",
        "Apply best practices to ensure code quality and testability",
        "Document implementation decisions and architecture",
        "Validate solution against real-world scenarios"
    ])

def get_prerequisites(week, day):
    """Return prerequisites for the specified day"""
    prerequisites = {
        (1, 1): [
            "Computer with at least 8GB RAM, 4 CPU cores, and 20GB free disk space",
            "Basic understanding of Git (cloning, committing, pushing)",
            "Familiarity with YAML syntax",
            "Terminal/command-line basics",
            "Administrator access to install software"
        ]
    }
    
    return prerequisites.get((week, day), [
        "Completion of previous day's tasks",
        "Working development environment",
        "Understanding of concepts covered previously",
        "Access to project repository",
        "Required tools and dependencies installed"
    ])

# Command line interface
if __name__ == "__main__":
    create_project_structure("Detect_Drift")