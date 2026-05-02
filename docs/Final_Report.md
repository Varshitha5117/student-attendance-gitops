# Final Year Project Report: Student Attendance System using GitOps

## 1. Project Overview
This project presents a **Student Attendance Web Application** fully deployed and managed using GitOps principles. The architecture ensures that a Git repository acts as the single source of truth for both the application code and the infrastructure declarative state. 

By integrating continuous integration (CI) via GitHub Actions, containerization with Docker, container orchestration via Kubernetes, and continuous deployment (CD) via Argo CD, this project achieves a highly scalable, version-controlled, and automated deployment pipeline.

## 2. Architecture Diagram & Workflow

```text
Developer -> GitHub (Source Code) -> GitHub Actions (CI) -> Docker Hub (Image Registry) -> GitHub (k8s manifests updated) -> Argo CD (CD Controller) -> Kubernetes Cluster
```

### The GitOps Loop:
1. **Source of Truth**: The developer pushes application code to the `main` branch.
2. **Continuous Integration**: GitHub Actions lint the code, build a Docker image, scan it with Trivy for vulnerabilities, and push the image to Docker Hub tagged with the Git SHA commit hash (`${{ github.sha }}`).
3. **Automated Manifest Update**: The CI pipeline updates the `deployment.yaml` with the new image tag and commits it back to the repository.
4. **Continuous Deployment**: Argo CD detects the drift between the cluster state and the Git repository. With **Auto-Sync** and **Self-Heal** enabled, it automatically pulls the changes and deploys the new image to Kubernetes.

## 3. Technology Stack
- **Frontend**: HTML5, Vanilla CSS
- **Backend**: Python Flask
- **Database**: PostgreSQL (Kubernetes deployed)
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **GitOps Controller**: Argo CD
- **CI/CD**: GitHub Actions
- **Security**: Trivy (Vulnerability Scanner)

## 4. One-Line Output Summary
**"The system provides a fully automated GitOps-based deployment pipeline where application updates are triggered by Git commits and deployed automatically to Kubernetes with real-time monitoring via Argo CD."**

## 5. Key DevOps Practices Implemented (Distinction Level)
- **Immutable Image Tags**: Avoided the `latest` tag anti-pattern. Instead, every deployment uses a unique, traceable Git SHA hash, enabling reproducible builds and easy rollbacks.
- **Git as the Single Source of Truth**: Changes to the Kubernetes cluster are exclusively made via Git commits, preventing manual configuration drift.
- **Automated Security Scanning**: Integrated Trivy to scan for OS and library vulnerabilities before pushing to the image registry.
- **Production-Ready Database**: Transitioned from a volatile SQLite DB to a robust PostgreSQL deployment running inside the Kubernetes cluster.
- **Self-Healing Infrastructure**: Argo CD continuously monitors the cluster. If manual changes are made (drift), Argo CD overwrites them to match the Git repository state.

## 6. Final Demo Instructions (For Viva/Presentation)
To impress the examiner, follow this exact workflow during the presentation:
1. **Show the Live Website**: Demonstrate the functional Student Attendance form and show the database working.
2. **Push a Small Code Change**: E.g., change `<h1>Student Attendance System</h1>` to `<h1>My College Attendance</h1>` in `app/templates/index.html`. Commit and push this to GitHub.
3. **Open the Argo CD Dashboard**: Show the examiner the live GitOps controller dashboard.
4. **Show Auto Deployment**: Wait 1-2 minutes and show the GitHub Actions pipeline succeeding, followed by Argo CD detecting the drift, and automatically syncing the new Pods.
5. **Refresh the Site**: Reload the live URL to immediately show the new `<h1>` title—all without any manual server deployment commands.
6. **Rollback (Optional)**: If asked, demonstrate reverting the Git commit. Argo CD will instantly redeploy the older version of the app.

## 7. Future Scope / Expansion
- **Monitoring**: Integrating **Prometheus** for metrics collection and **Grafana** for dashboard visualization.
- **Ingress Controller**: Exposing the application securely via an Ingress controller with TLS termination instead of a basic NodePort.
- **Secret Management**: Implementing HashiCorp Vault or External Secrets Operator for handling the PostgreSQL credentials securely rather than passing them via environment variables.

---

# Viva Q&A Sheet

### Q1: What is GitOps and how is it different from traditional CI/CD?
**Answer**: GitOps is a modern DevOps practice where a Git repository is the single source of truth for infrastructure and applications. While traditional CI/CD pushes changes directly to the cluster (Push model), GitOps uses a software agent (like Argo CD) inside the cluster to pull the declarative state from Git (Pull model). This improves security, as CI pipelines don't need cluster credentials.

### Q2: Why are you using `${{ github.sha }}` for image tagging instead of `latest`?
**Answer**: Using `latest` is an anti-pattern because it is mutable. If `latest` breaks, it's hard to know exactly which code caused it or how to roll back. By using the Git commit SHA, every image is uniquely tied to a specific point in the source code, making deployments deterministic, reproducible, and easy to roll back.

### Q3: Explain how Argo CD works in your project.
**Answer**: Argo CD runs as a controller inside the Kubernetes cluster. It continuously polls our GitHub repository. When GitHub Actions commits the new image tag to `deployment.yaml`, Argo CD detects a difference between the desired state in Git and the actual state in the cluster. Because Auto-Sync is enabled, it automatically applies the new YAML, rolling out the new pods.

### Q4: What happens if someone manually changes a configuration inside the Kubernetes cluster using `kubectl`?
**Answer**: Because we configured Argo CD with **Self-Heal**, if someone makes an unauthorized manual change to the cluster (e.g., changing replicas or image tags), Argo CD will immediately detect the drift and overwrite the manual change to ensure the cluster matches the Git repository (the single source of truth).

### Q5: Why did you choose PostgreSQL over SQLite?
**Answer**: SQLite stores data in a local file. In a Kubernetes environment, pods are ephemeral. If a pod restarts or scales up, the SQLite database is lost or out of sync. PostgreSQL allows for a centralized, persistent data layer that multiple replicas of our Flask app can connect to securely.

### Q6: How are you ensuring the security of your Docker images?
**Answer**: I have integrated Trivy into the GitHub Actions CI pipeline. Before the Docker image is pushed to the registry, Trivy scans it for known vulnerabilities (CVEs) in the OS packages and libraries. This represents a "Shift-Left" security approach.
