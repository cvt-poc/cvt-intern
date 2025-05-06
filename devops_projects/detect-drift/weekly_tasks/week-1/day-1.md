# Week 1 Day 1: Introduction to GitOps and Configuration Drift

## Overview
- **Duration**: Full day (8 hours)
- **Why This Matters**: Configuration drift is one of the most common yet challenging problems in modern infrastructure management. When live environments don't match their declared state in version control, it leads to inconsistent environments, failed deployments, security vulnerabilities, and difficult-to-diagnose production issues. As a DevOps/SRE professional, understanding and managing drift is essential for maintaining reliable systems.
- **Connection to Project**: Today establishes the foundation for our Detect_Drift tool by understanding the problem space, exploring existing approaches, and defining our unique value proposition. Without this conceptual foundation, we can't build an effective solution.

## Learning Objectives
By the end of today, you will be able to:
1. Explain the concept of configuration drift and its impact on DevOps practices
2. Describe the principles of GitOps and how they relate to drift detection
3. Compare at least three existing approaches to drift detection and their limitations
4. Set up a basic local Kubernetes environment with a Git repository
5. Manually create and detect a simple case of configuration drift

## Prerequisites
- Computer with at least 8GB RAM, 4 CPU cores, and 20GB free disk space
- Basic understanding of Git (cloning, committing, pushing)
- Familiarity with YAML syntax
- Terminal/command-line basics
- Administrator access to install software

## Morning Session (4 hours)

### Technical Concept Deep Dive (90 minutes)

#### Key Concept 1: Understanding Configuration Drift
Configuration drift occurs when the actual state of your infrastructure (particularly Kubernetes clusters) diverges from the declared state in your source code repository. This divergence can happen for various reasons:

**Common causes of drift:**
- Manual changes made directly to the cluster (using kubectl edit/patch/apply)
- Automated changes from operators or controllers not tracked in Git
- Failed partial deployments
- Resource modifications by maintenance scripts
- Emergency hotfixes that bypass normal workflows

**Real-world impact:**
```yaml
# What's in Git:
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-config
data:
  MAX_CONNECTIONS: "100"
  TIMEOUT_SECONDS: "30"
  
# What's in the cluster after emergency hotfix:
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-config
data:
  MAX_CONNECTIONS: "500"  # Changed during outage
  TIMEOUT_SECONDS: "120"  # Changed during outage
```

When the next deployment runs, these emergency changes will be overwritten, potentially causing another outage. Without drift detection, no one may even realize this risk exists.

**Drift categories:**
1. **Benign drift**: Non-critical differences (e.g., auto-generated fields, timestamps)
2. **Significant drift**: Changes that affect behavior but aren't immediately harmful
3. **Critical drift**: Changes that could cause outages or security vulnerabilities if reverted

#### Key Concept 2: GitOps Principles
GitOps is a set of practices where the entire system is described declaratively in Git:

**Core GitOps principles:**
1. **Declarative configuration**: The desired system state is fully described in code
2. **Version controlled**: All changes are tracked in Git with history, attribution, and rollback capability
3. **Automated application**: Changes approved in Git are automatically applied to the system
4. **Continuous reconciliation**: The system constantly works to ensure the actual state matches the desired state

**GitOps workflow:**
```
┌────────────┐     ┌─────────────┐     ┌────────────────┐
│ Developer  │────►│ Git         │────►│ GitOps         │
│ makes      │     │ repository  │     │ controller     │
│ changes    │     │ with desired│     │ (ArgoCD/Flux)  │
└────────────┘     │ state       │     └────────┬───────┘
                   └─────────────┘              │
                          ▲                     │
                          │                     │
                          │                     ▼
┌─────────────┐     ┌─────┴───────┐     ┌────────────────┐
│ Detect_Drift│     │ Drift       │     │ Kubernetes     │
│ tool reports│◄────┤ detection   │◄────┤ cluster        │
│ and alerts  │     │ process     │     │ (actual state) │
└─────────────┘     └─────────────┘     └────────────────┘
```

**Common misconception**: Many teams implement only half of GitOps - they deploy from Git but don't implement the continuous reconciliation loop or drift detection, which leaves them vulnerable to configuration drift.

#### Key Concept 3: Current Approaches to Drift Detection

**Approach 1: Manual Comparison**
```bash
# Extract config from Git
git show master:deployment.yaml > git-deployment.yaml

# Extract config from cluster
kubectl get deployment myapp -o yaml > cluster-deployment.yaml

# Compare the files
diff git-deployment.yaml cluster-deployment.yaml
```

**Limitations**: Time-consuming, error-prone, not scalable, difficult to automate

**Approach 2: GitOps Controllers (ArgoCD/Flux)**
```
ArgoCD continuously compares Git state to cluster state:

status:
  conditions:
  - lastTransitionTime: "2023-05-01T10:00:00Z"
    message: Healthy
    reason: Synced
    status: "True"
    type: Healthy
  - lastTransitionTime: "2023-05-01T10:00:00Z"
    message: "Resources are out of sync with Git"
    reason: OutOfSync
    status: "False"
    type: Synced
```

**Limitations**: Limited to resources managed by the controller, often lacks detailed policy controls, drift reporting is basic

**Approach 3: Custom Scripts**
Organizations often develop custom scripts to detect drift for specific resources or configurations.

**Limitations**: Maintenance burden, limited scope, inconsistent implementation

**Approach 4: Commercial Solutions**
Several vendors offer drift detection tools with advanced features.

**Limitations**: Often expensive, may be tied to specific platforms, can be complex to implement

#### Self-Check Questions
1. What is configuration drift and why is it important to detect and manage it?
2. How do the four GitOps principles help prevent configuration drift?
3. What are the limitations of relying solely on a GitOps controller like ArgoCD for drift detection?
4. What categories of drift should we consider when designing a drift detection solution?
5. How does the concept of "immutability" relate to configuration drift?

### Hands-on Exploration (2.5 hours)

#### Setup (30 minutes)
Let's set up our local environment with the tools we'll need throughout this project:

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube-linux-amd64
sudo mv minikube-linux-amd64 /usr/local/bin/minikube

# Start minikube
minikube start

# Verify installation
kubectl get nodes
minikube status

# Create project directory
mkdir -p ~/projects/detect-drift
cd ~/projects/detect-drift

# Initialize Git repository
git init
```

#### Exercise 1: Creating and Deploying a Simple Application (45 minutes)

1. Create a simple deployment manifest:

```bash
cat > deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
EOF
```

2. Add this file to Git:

```bash
git add deployment.yaml
git commit -m "Add initial nginx deployment"
```

3. Deploy to Kubernetes:

```bash
kubectl apply -f deployment.yaml
```

4. Verify deployment:

```bash
kubectl get deployments
kubectl get pods
```

#### Exercise 2: Manually Creating and Detecting Drift (45 minutes)

1. Let's create drift by directly modifying the cluster:

```bash
# Scale the deployment using kubectl
kubectl scale deployment nginx-deployment --replicas=4

# Check the current state
kubectl get deployment nginx-deployment -o yaml
```

2. Now compare with our Git version:

```bash
# View what's in Git
cat deployment.yaml

# Extract deployment from cluster
kubectl get deployment nginx-deployment -o yaml > cluster-deployment.yaml

# Compare the files
diff deployment.yaml cluster-deployment.yaml
```

3. Observe differences, focusing on:
   - The replicas field (changed from 2 to 4)
   - Auto-generated fields (like status, resourceVersion, etc.)
   
4. Document these differences, categorizing them as:
   - Significant drift (replicas count change)
   - Benign drift (auto-generated fields)

#### Exercise 3: Exploring GitOps Controllers (60 minutes)

1. Install ArgoCD in your cluster:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=300s
```

2. Access the ArgoCD UI:

```bash
# Port forward to access the UI
kubectl port-forward svc/argocd-server -n argocd 8080:443 &

# Get the initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

3. Open your browser at https://localhost:8080 and log in with:
   - Username: admin
   - Password: (from the previous command)

4. Create a simple application in ArgoCD:
   - Use your local Git repository path
   - Target namespace: default
   - Choose automatic sync policy
   
5. Create additional drift and observe how ArgoCD detects and reports it:

```bash
# Change the image version
kubectl set image deployment/nginx-deployment nginx=nginx:1.20
```

6. Observe in the ArgoCD UI how it shows the deployment as "Out of sync"

7. Document the drift detection capabilities of ArgoCD:
   - What information does it provide?
   - How easy is it to identify the specific drift?
   - What actions can you take directly from the UI?

## Afternoon Session (4 hours)

### Implementation Challenge (3 hours)

#### Task Description
Your first challenge is to create a basic script that can detect drift between a Kubernetes manifest file in Git and the actual state in your cluster. This script will form the foundation of our Detect_Drift tool.

#### Requirements
- The script should accept a file path to a Kubernetes manifest
- It should retrieve the corresponding resource from the cluster
- It should compare the two and identify differences
- It should categorize differences as either "significant" or "benign"
- It should output a summary of the differences

#### Implementation Steps

1. Create a new Python script:

```bash
touch drift_detector.py
chmod +x drift_detector.py
```

2. Implement the script:

```python
#!/usr/bin/env python3
import subprocess
import sys
import yaml
import json
import tempfile

def run_command(command):
    """Run a shell command and return the output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
        sys.exit(1)
    return result.stdout

def get_resource_from_file(file_path):
    """Load a Kubernetes resource from a file"""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def get_resource_from_cluster(resource_type, resource_name, namespace='default'):
    """Get a resource from the Kubernetes cluster"""
    command = f"kubectl get {resource_type} {resource_name} -n {namespace} -o json"
    output = run_command(command)
    return json.loads(output)

def is_benign_field(field_path):
    """Determine if a field difference is benign"""
    benign_fields = [
        "status",
        "metadata.resourceVersion",
        "metadata.uid",
        "metadata.generation",
        "metadata.creationTimestamp",
        "metadata.selfLink",
        "metadata.managedFields",
        "spec.template.metadata.creationTimestamp"
    ]
    
    for benign_field in benign_fields:
        if field_path.startswith(benign_field):
            return True
    return False

def compare_resources(git_resource, cluster_resource, path=""):
    """Compare two resources recursively and return differences"""
    differences = []
    
    # Handle different types
    if type(git_resource) != type(cluster_resource):
        differences.append({
            "path": path,
            "git_value": git_resource,
            "cluster_value": cluster_resource,
            "benign": False
        })
        return differences
    
    # Handle dictionaries
    if isinstance(git_resource, dict):
        git_keys = set(git_resource.keys())
        cluster_keys = set(cluster_resource.keys())
        
        # Find keys in git but not in cluster
        for key in git_keys - cluster_keys:
            differences.append({
                "path": f"{path}.{key}" if path else key,
                "git_value": git_resource[key],
                "cluster_value": None,
                "benign": False
            })
        
        # Find keys in cluster but not in git
        for key in cluster_keys - git_keys:
            new_path = f"{path}.{key}" if path else key
            differences.append({
                "path": new_path,
                "git_value": None,
                "cluster_value": cluster_resource[key],
                "benign": is_benign_field(new_path)
            })
        
        # Compare values for common keys
        for key in git_keys & cluster_keys:
            new_path = f"{path}.{key}" if path else key
            differences.extend(compare_resources(git_resource[key], cluster_resource[key], new_path))
        
        return differences
    
    # Handle lists
    if isinstance(git_resource, list):
        # This is a simplified approach for lists - in a real implementation, 
        # you would need more sophisticated matching logic
        if len(git_resource) != len(cluster_resource):
            differences.append({
                "path": path,
                "git_value": git_resource,
                "cluster_value": cluster_resource,
                "benign": False
            })
        else:
            for i in range(len(git_resource)):
                differences.extend(compare_resources(git_resource[i], cluster_resource[i], f"{path}[{i}]"))
        
        return differences
    
    # Handle primitive values
    if git_resource != cluster_resource:
        differences.append({
            "path": path,
            "git_value": git_resource,
            "cluster_value": cluster_resource,
            "benign": is_benign_field(path)
        })
    
    return differences

def main():
    if len(sys.argv) < 2:
        print("Usage: ./drift_detector.py <manifest_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    git_resource = get_resource_from_file(file_path)
    
    resource_kind = git_resource["kind"].lower()
    resource_name = git_resource["metadata"]["name"]
    namespace = git_resource["metadata"].get("namespace", "default")
    
    try:
        cluster_resource = get_resource_from_cluster(resource_kind, resource_name, namespace)
    except Exception as e:
        print(f"Error: Resource {resource_kind}/{resource_name} not found in the cluster")
        print(e)
        sys.exit(1)
    
    differences = compare_resources(git_resource, cluster_resource)
    
    # Categorize and display differences
    significant_diffs = [d for d in differences if not d["benign"]]
    benign_diffs = [d for d in differences if d["benign"]]
    
    print(f"\nDrift Detection Results for {resource_kind}/{resource_name}:")
    print("=" * 50)
    
    if not differences:
        print("No drift detected! Git and cluster states match.")
        sys.exit(0)
    
    print(f"Total differences: {len(differences)}")
    print(f"Significant differences: {len(significant_diffs)}")
    print(f"Benign differences: {len(benign_diffs)}")
    
    if significant_diffs:
        print("\nSignificant Differences:")
        print("-" * 30)
        for diff in significant_diffs:
            print(f"Path: {diff['path']}")
            print(f"  Git value: {diff['git_value']}")
            print(f"  Cluster value: {diff['cluster_value']}")
            print()
    
    if benign_diffs:
        print("\nBenign Differences (auto-generated fields, etc.):")
        print("-" * 30)
        for diff in benign_diffs[:3]:  # Only show first 3 benign differences to avoid clutter
            print(f"Path: {diff['path']}")
        if len(benign_diffs) > 3:
            print(f"...and {len(benign_diffs) - 3} more benign differences")

if __name__ == "__main__":
    main()
```

3. Test the script with our deployment:

```bash
# Fix the deployment in Git to match our expected state
cat > deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
EOF

# Commit the changes
git add deployment.yaml
git commit -m "Update deployment file to match expected state"

# Run our drift detector
python3 drift_detector.py deployment.yaml
```

4. Observe the output and note how the script detects and categorizes differences.

5. Try creating different types of drift and observe how the script handles them:

```bash
# Change container resource limits
kubectl set resources deployment nginx-deployment --containers=nginx --limits=cpu=200m,memory=256Mi

# Run the detector again
python3 drift_detector.py deployment.yaml
```

#### Expected Deliverables
- Working drift detection script (drift_detector.py)
- Documentation of the script's approach and limitations
- Example outputs showing different types of drift detection

#### Testing and Validation
- The script should correctly identify replicas drift
- The script should correctly identify image version drift
- The script should correctly identify resource limits drift
- The script should ignore auto-generated fields like status and resourceVersion

### Documentation and Reflection (1 hour)

#### Documentation Tasks
- Create a README.md file for your drift detector:

```bash
cat > README.md << 'EOF'
# Drift Detector

A simple tool to detect configuration drift between Kubernetes manifests in Git and live clusters.

## Overview

This script compares Kubernetes resources defined in Git with their actual state in a Kubernetes cluster to identify "drift" - differences between the desired and actual states.

## Features

- Detects differences between Git manifests and cluster resources
- Categorizes differences as "significant" or "benign"
- Generates a summary report of all differences

## Usage

```
./drift_detector.py <manifest_file>
```

## Limitations

This initial implementation has several limitations:
- Only supports single-resource files
- Uses a simplistic approach for comparing lists
- Doesn't handle custom resources with special drift rules
- Limited to resources defined explicitly in the file

## Future Improvements

- Support for multiple resources in a single file
- Better handling of list comparisons using resource identifiers
- Support for directory scanning to check multiple resources
- Integration with Git operations to show changes over time
- Policy support for custom drift rules
```

The future improvements section should contain features you intend to implement in the coming weeks.
EOF
```

- Document any challenges you encountered while implementing the script
- Create a journal entry about what you learned today

#### Reflection Questions
1. What surprised you about detecting configuration drift?
2. How does the approach we've implemented compare to what ArgoCD does?
3. What types of drift do you think would be most critical in a production environment?
4. What improvements would make our drift detector more useful?
5. How could we extend this to work with multiple resources or entire directories?

## Resources

### Essential Reading
- [GitOps: What You Need to Know](https://www.weave.works/blog/gitops-what-you-need-to-know)
- [Kubernetes Documentation: Working with kubectl](https://kubernetes.io/docs/reference/kubectl/)
- [ArgoCD Documentation: Sync Status](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-status/)

### Reference Documentation
- [Kubernetes API Overview](https://kubernetes.io/docs/reference/using-api/)
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Python subprocess module](https://docs.python.org/3/library/subprocess.html)

### Video Tutorials
- [Introduction to GitOps with ArgoCD](https://www.youtube.com/watch?v=MeU5_k9ssrs)
- [Kubernetes Configuration Management](https://www.youtube.com/watch?v=Nm_WYwZEjQw)
- [Configuration Drift in Kubernetes](https://www.youtube.com/watch?v=6sVDcUGQjE0)

### Code Examples
- [Kubernetes Python Client Examples](https://github.com/kubernetes-client/python/tree/master/examples)
- [Advanced YAML Parsing in Python](https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation)

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| kubectl not configured | "The connection to the server localhost:8080 was refused" | Run `minikube start` to ensure the cluster is running |
| Resource not found | "Error: Resource deployment/nginx-deployment not found in the cluster" | Check resource name and namespace, verify it was created correctly |
| JSON parsing error | "JSONDecodeError" | Verify the kubectl command is returning valid JSON |
| Script permission denied | "Permission denied" when running the script | Run `chmod +x drift_detector.py` |
| PyYAML not installed | "ModuleNotFoundError: No module named 'yaml'" | Install with `pip install pyyaml` |

## Mentorship and Support

### Scheduled Check-ins
- Morning kickoff (9:00 AM): Review the day's plan and clarify objectives
- Midday check (12:30 PM): Verify morning exercises completion and address any issues
- End-of-day review (4:30 PM): Evaluate script implementation and answer questions

### When to Ask for Help
- You've been stuck on the same issue for more than 30 minutes
- You're unsure about how to interpret differences between Git and cluster states
- Your script is producing unexpected results or errors
- You need clarification on GitOps concepts or Kubernetes behavior

### How to Ask for Help Effectively
- Clearly describe what you're trying to achieve
- Share your current code or approach
- Explain what you've already tried
- Include error messages or unexpected outputs

## Extension Activities

If you complete the day's tasks early, challenge yourself with:
- Extend the script to handle multiple resources in a single YAML file (using `---` separators)
- Add support for custom drift rules defined in a configuration file
- Implement a more sophisticated approach for comparing lists in Kubernetes resources
- Create a simple visualization of the drift using ASCII art or terminal colors

## Preparation for Tomorrow

To prepare for tomorrow's tasks:
- Review the Python code we created today
- Read about Kubernetes resource types and their relationships
- Think about how we could automate the drift detection process
- Consider how we might structure a more comprehensive tool

## Success Criteria

You have successfully completed today's tasks when:
1. You can explain the concept of configuration drift and its impact
2. You have a working drift detection script that identifies differences
3. Your script correctly categorizes differences as significant or benign
4. You've documented the approach and limitations of your implementation
5. You can run the script against different resources and interpret the results
6. You've committed all code and documentation to your Git repository