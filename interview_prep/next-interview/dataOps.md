# DataOps Interview Preparation — Git/GitHub & Jenkins (Data Engineer)

> A comprehensive guide covering DataOps concepts, Git/GitHub version control, CI/CD pipelines, and Jenkins automation commonly asked in Data Engineering interviews.

---

## 📋 Topics Covered

- What is DataOps
- Git Core Concepts
- Git Branching Strategies
- GitHub Features for Data Engineering
- GitHub Actions (CI/CD)
- Pull Requests & Code Review
- What is CI/CD in Data Engineering
- What is Jenkins
- Jenkins Architecture
- Jenkins Pipelines
- Jenkins for Data Pipelines
- GitHub Actions vs Jenkins
- Common Interview Questions & Answers

---

## PART 1 — Git & GitHub

---

## 1. What is DataOps?

**DataOps** is a set of practices, processes, and technologies that combines **Agile development, DevOps, and data engineering** to improve the speed, quality, and reliability of data pipelines and analytics.

It applies software engineering best practices — version control, automated testing, CI/CD — to **data pipelines and data workflows**.

### Core Principles of DataOps

| Principle | Description |
|---|---|
| **Version control** | All pipeline code, configs, and SQL tracked in Git |
| **Automated testing** | Data quality checks run automatically before deployment |
| **CI/CD** | Pipelines built, tested, and deployed automatically |
| **Collaboration** | Shared codebase, code reviews, pull requests |
| **Monitoring** | Pipelines observed and alerted on in production |
| **Repeatability** | Environments reproducible — same result every run |

### DataOps vs DevOps

| Feature | DevOps | DataOps |
|---|---|---|
| Focus | Application software | Data pipelines and workflows |
| Output | Running applications | Reliable data products |
| Testing | Unit/integration tests | Data quality + pipeline tests |
| Key tools | Jenkins, GitHub Actions | Airflow, dbt, Great Expectations |
| Deployment | Code releases | Pipeline and schema changes |

---

## 2. What is Git?

**Git** is a **distributed version control system** that tracks changes in source code (or any text files) over time. It allows multiple developers to collaborate on the same codebase without overwriting each other's work.

Every developer has a **full copy of the repository** including its entire history — no central dependency.

### Why Git is Essential for Data Engineers

- Track changes to **pipeline code, SQL transformations, config files**
- Collaborate with teammates without conflicts
- Roll back to previous working versions when bugs are introduced
- Review changes before they reach production
- Automate testing and deployment through CI/CD triggers

### Git vs GitHub vs GitLab vs Bitbucket

| Tool | Type | Description |
|---|---|---|
| **Git** | Version control system | The tool itself — runs locally |
| **GitHub** | Cloud hosting platform | Host Git repos, PRs, Actions |
| **GitLab** | Cloud hosting platform | Similar to GitHub, built-in CI/CD |
| **Bitbucket** | Cloud hosting platform | Atlassian product, integrates with Jira |
| **Azure DevOps** | Cloud hosting platform | Microsoft ecosystem |

---

## 3. Core Git Concepts

### Repository (Repo)

A **repository** is a directory tracked by Git — contains all files and the complete history of every change ever made.

```bash
# Initialize a new repo
git init my_pipeline_project

# Clone an existing repo
git clone https://github.com/org/data-pipelines.git
```

### Commit

A **commit** is a snapshot of all tracked files at a point in time — the fundamental unit of Git history.

```bash
# Stage files for commit
git add pipeline.py
git add dbt/models/

# Commit with a message
git commit -m "feat: add daily sales aggregation pipeline"

# Stage and commit all tracked changes
git commit -am "fix: handle null values in transaction_date"
```

### Good Commit Message Conventions

```
feat:     New feature or pipeline
fix:      Bug fix
refactor: Code restructure, no behavior change
test:     Add or update tests
docs:     Documentation update
chore:    Config, dependency, or tooling change
ci:       CI/CD pipeline changes

Examples:
feat: add snowflake ingestion pipeline for CRM data
fix: resolve data skew in customer join
refactor: split large transform into smaller dbt models
test: add great expectations suite for sales table
```

### Staging Area

The **staging area** (index) is where you prepare changes before committing.

```bash
# Check what is staged vs unstaged
git status

# See unstaged changes
git diff

# See staged changes
git diff --staged

# Unstage a file
git restore --staged pipeline.py
```

### Git Log & History

```bash
# View commit history
git log

# Compact one-line view
git log --oneline --graph

# View changes in a specific commit
git show abc1234

# View who changed each line (blame)
git blame dbt/models/sales.sql
```

---

## 4. Git Branching

**Branches** allow parallel development — work on features or fixes in isolation without affecting the main codebase.

### Core Branch Commands

```bash
# List all branches
git branch -a

# Create a new branch
git branch feature/add-aurora-connector

# Switch to a branch
git checkout feature/add-aurora-connector

# Create and switch in one command
git checkout -b feature/add-aurora-connector

# Rename current branch
git branch -m new-branch-name

# Delete a branch (after merge)
git branch -d feature/add-aurora-connector
```

### Merging vs Rebasing

| Feature | Merge | Rebase |
|---|---|---|
| History | Preserves full history with merge commit | Linear, cleaner history |
| Conflict handling | Resolved once at merge | Resolved commit by commit |
| Use case | Feature branches merging to main | Keeping feature branch up-to-date |
| Safety | Safer — non-destructive | Rewrites history — avoid on shared branches |

```bash
# Merge feature branch into main
git checkout main
git merge feature/add-aurora-connector

# Rebase feature branch on top of main
git checkout feature/add-aurora-connector
git rebase main
```

### Resolving Merge Conflicts

```bash
# After a conflict is flagged
git status                       # See conflicted files

# Edit the file — remove conflict markers
# <<<<<<< HEAD
# your changes
# =======
# incoming changes
# >>>>>>> feature/branch

git add resolved_file.py         # Mark as resolved
git commit                       # Complete the merge
```

---

## 5. Git Branching Strategies

### GitFlow

A structured branching model with dedicated branches for features, releases, and hotfixes.

```
main          ──────────────────────────────────► (production)
                  ↑                    ↑
release/1.0 ──────┘                    │
                  ↑                    │
develop   ────────────────────────────►│
              ↑         ↑
feature/A ────┘         │
feature/B ──────────────┘
```

| Branch | Purpose |
|---|---|
| `main` | Production-ready code only |
| `develop` | Integration branch for features |
| `feature/*` | Individual feature development |
| `release/*` | Prep for a new release |
| `hotfix/*` | Emergency production fixes |

### Trunk-Based Development

All developers commit directly to `main` (or short-lived branches merged within a day).

```
main  ──────────────────────────────────►
        ↑   ↑   ↑   ↑
       f1  f2  f3  hotfix  (all merged quickly)
```

- Preferred for teams with strong CI/CD
- Reduces merge conflicts
- Enables continuous deployment

### GitHub Flow (Simplified)

```
main ──────────────────────────────────►
          ↑            ↑
   feature/A      feature/B
   (PR → review → merge)
```

Simple two-level model — feature branches off main, merged via Pull Request. Common in data engineering teams.

---

## 6. What is GitHub?

**GitHub** is a cloud-based platform for **hosting Git repositories and collaborating on code**. It adds a web interface, collaboration tools, and automation on top of Git.

### Key GitHub Features for Data Engineers

| Feature | Description |
|---|---|
| **Repositories** | Host pipeline code, dbt models, SQL, configs |
| **Pull Requests** | Propose, review, and merge code changes |
| **Issues** | Track bugs, tasks, and feature requests |
| **GitHub Actions** | Built-in CI/CD automation |
| **Branch Protection** | Enforce PR reviews before merging to main |
| **Secrets** | Store credentials securely for CI/CD |
| **GitHub Packages** | Host Python packages or Docker images |
| **GitHub Pages** | Host documentation sites |

### Remote Repository Commands

```bash
# Add a remote
git remote add origin https://github.com/org/data-pipelines.git

# Push a branch to remote
git push origin feature/aurora-connector

# Pull latest changes
git pull origin main

# Fetch without merging
git fetch origin

# Push and set upstream tracking
git push -u origin feature/aurora-connector
```

---

## 7. Pull Requests & Code Review

A **Pull Request (PR)** is a GitHub mechanism to propose merging changes from one branch into another — enabling **code review, discussion, and automated checks** before merging.

### PR Workflow in Data Engineering

```
1. Create feature branch
        ↓
2. Write pipeline code / dbt models / SQL
        ↓
3. Push branch to GitHub
        ↓
4. Open Pull Request → describe changes
        ↓
5. Automated CI checks run (tests, linting)
        ↓
6. Peer code review — comments, approvals
        ↓
7. Merge to main
        ↓
8. CD pipeline deploys to production
```

### Good PR Practices

- Keep PRs **small and focused** — one feature or fix per PR
- Write a clear **description** of what changed and why
- Link to related **issues or tickets**
- Add **screenshots or query results** for data changes
- Ensure all **CI checks pass** before requesting review
- **Respond to comments** promptly

### Branch Protection Rules (GitHub Settings)

```
✅ Require pull request before merging
✅ Require at least 1 approving review
✅ Require status checks to pass (CI tests)
✅ Require branches to be up to date
✅ Restrict who can push to main
```

---

## 8. What is CI/CD in Data Engineering?

**CI/CD (Continuous Integration / Continuous Deployment)** is the practice of **automatically testing and deploying data pipelines** whenever code changes are pushed.

### Continuous Integration (CI)

Automatically runs tests and checks every time code is pushed or a PR is opened.

| CI Check | Description |
|---|---|
| **Unit tests** | Test individual transformation functions |
| **SQL linting** | Check SQL style and syntax (sqlfluff) |
| **dbt compile** | Validate dbt models compile without errors |
| **Data quality tests** | Run Great Expectations or dbt tests |
| **Code linting** | Python style checks (flake8, black) |
| **Security scan** | Check for hardcoded credentials |

### Continuous Deployment (CD)

Automatically deploys the pipeline to staging or production after CI passes.

| CD Step | Description |
|---|---|
| **Deploy to staging** | Run pipeline in a staging environment first |
| **Smoke tests** | Validate output in staging |
| **Deploy to production** | Push validated code to production |
| **Notify team** | Slack/email notification on deploy |

### CI/CD Triggers

```
Push to feature branch    → Run CI tests only
Open Pull Request         → Run CI + post results to PR
Merge to main             → Run CI + deploy to staging
Tag a release             → Deploy to production
```

---

## PART 2 — Jenkins

---

## 9. What is Jenkins?

**Jenkins** is an **open-source automation server** used to build, test, and deploy software automatically. It is one of the most widely used CI/CD tools in the industry.

In data engineering, Jenkins automates the **build, test, and deployment of data pipelines**, ETL jobs, and data transformation code.

### Key Features

| Feature | Description |
|---|---|
| **Open source** | Free, large community, extensive plugins |
| **Plugin ecosystem** | 1,800+ plugins for tools like Git, Docker, AWS, Slack |
| **Pipeline as code** | Define CI/CD pipelines in a `Jenkinsfile` |
| **Distributed builds** | Master-agent architecture for parallel jobs |
| **Scheduling** | Built-in cron-based job scheduling |
| **Integration** | Works with GitHub, GitLab, Bitbucket, Jira |
| **Self-hosted** | Full control — runs on your own infrastructure |

---

## 10. Jenkins Architecture

```
┌─────────────────────────────────────────────────┐
│               JENKINS MASTER                    │
│                                                 │
│  ┌─────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Job     │  │  Build   │  │   Plugin      │  │
│  │ Config  │  │  Queue   │  │   Manager     │  │
│  └─────────┘  └──────────┘  └───────────────┘  │
│                    │                            │
└────────────────────┼────────────────────────────┘
                     │ Distributes tasks
        ┌────────────┼────────────┐
        ↓            ↓            ↓
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │  AGENT 1 │ │  AGENT 2 │ │  AGENT 3 │
  │(Linux)   │ │(Docker)  │ │(Windows) │
  └──────────┘ └──────────┘ └──────────┘
```

### Master (Controller)

- Hosts Jenkins UI and configuration
- Manages build queue and scheduling
- Delegates build jobs to agents
- Stores build history and logs

### Agents (Workers)

- Execute the actual build/test/deploy steps
- Can run on different OS or environments
- Can be spun up in Docker or Kubernetes
- Multiple agents allow **parallel execution**

---

## 11. Jenkinsfile — Pipeline as Code

A **Jenkinsfile** defines the CI/CD pipeline as code — stored in the repository alongside the pipeline code itself.

### Declarative Pipeline Syntax

```groovy
pipeline {
    agent any

    environment {
        SNOWFLAKE_ACCOUNT = credentials('snowflake-account')
        AWS_CREDENTIALS   = credentials('aws-access-key')
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/org/data-pipelines.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                sh 'flake8 pipelines/'
                sh 'sqlfluff lint dbt/models/'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest tests/ -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('dbt Compile & Test') {
            steps {
                sh 'dbt compile --profiles-dir ./profiles'
                sh 'dbt test --profiles-dir ./profiles'
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh 'dbt run --target staging --profiles-dir ./profiles'
            }
        }

        stage('Deploy to Production') {
            when {
                tag 'release-*'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                sh 'dbt run --target prod --profiles-dir ./profiles'
            }
        }
    }

    post {
        success {
            slackSend channel: '#data-eng',
                      message: "✅ Pipeline ${env.JOB_NAME} deployed successfully"
        }
        failure {
            slackSend channel: '#data-eng',
                      message: "❌ Pipeline ${env.JOB_NAME} failed — check logs"
        }
    }
}
```

### Scripted Pipeline Syntax

```groovy
node {
    stage('Extract') {
        sh 'python extract.py'
    }
    stage('Transform') {
        sh 'python transform.py'
    }
    stage('Load') {
        sh 'python load.py'
    }
}
```

> **Declarative** is preferred — more structured, readable, and supports built-in directives like `when`, `parallel`, and `post`.

---

## 12. Jenkins for Data Pipelines

### Triggering Jenkins Jobs

```groovy
// Trigger on GitHub push
triggers {
    githubPush()
}

// Trigger on a schedule (cron)
triggers {
    cron('0 2 * * *')    // Every day at 2 AM
}

// Poll SCM for changes
triggers {
    pollSCM('H/5 * * * *')    // Check for changes every 5 minutes
}
```

### Parallel Stages

Run independent pipeline stages simultaneously:

```groovy
stage('Parallel Tests') {
    parallel {
        stage('Unit Tests') {
            steps { sh 'pytest tests/unit/' }
        }
        stage('Data Quality Tests') {
            steps { sh 'great_expectations checkpoint run sales_checkpoint' }
        }
        stage('SQL Lint') {
            steps { sh 'sqlfluff lint dbt/models/' }
        }
    }
}
```

### Environment-Specific Deployments

```groovy
stage('Deploy') {
    steps {
        script {
            def target_env = env.BRANCH_NAME == 'main' ? 'staging' : 'dev'
            sh "dbt run --target ${target_env}"
        }
    }
}
```

### Using Docker Agents

Run jobs inside Docker containers for consistent environments:

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Run Spark Job') {
            steps {
                sh 'pip install pyspark'
                sh 'python spark_pipeline.py'
            }
        }
    }
}
```

---

## 13. GitHub Actions

**GitHub Actions** is GitHub's **built-in CI/CD platform** — define workflows in YAML files stored in `.github/workflows/`.

### Example — Data Pipeline CI Workflow

```yaml
# .github/workflows/ci.yml

name: Data Pipeline CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:

  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint Python
        run: flake8 pipelines/

      - name: Run unit tests
        run: pytest tests/ -v

      - name: Lint SQL (sqlfluff)
        run: sqlfluff lint dbt/models/

  dbt-checks:
    runs-on: ubuntu-latest
    needs: lint-and-test

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dbt
        run: pip install dbt-snowflake

      - name: dbt compile
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
        run: dbt compile --profiles-dir ./profiles

      - name: dbt test
        run: dbt test --profiles-dir ./profiles

  deploy-staging:
    runs-on: ubuntu-latest
    needs: dbt-checks
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to staging
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
        run: dbt run --target staging --profiles-dir ./profiles
```

---

## 14. GitHub Actions vs Jenkins

| Feature | GitHub Actions | Jenkins |
|---|---|---|
| Hosting | Cloud (GitHub-managed) | Self-hosted |
| Setup | Zero setup — built into GitHub | Requires installation & maintenance |
| Config format | YAML | Groovy (Jenkinsfile) |
| Cost | Free for public repos, paid minutes for private | Free (infrastructure cost only) |
| Plugin ecosystem | GitHub Marketplace actions | 1,800+ plugins |
| Scalability | Auto-scales (GitHub runners) | Manual agent management |
| Secrets management | GitHub Secrets (built-in) | Jenkins Credentials plugin |
| Integration | Native GitHub (PRs, branches, tags) | Webhooks, plugins |
| Docker support | Yes | Yes |
| Best for | GitHub-hosted projects, modern teams | On-premise, enterprise, complex pipelines |
| Learning curve | Low | Medium–High |

### When to Choose Which

**Choose GitHub Actions when:**
- Your code is already on GitHub
- You want zero-maintenance CI/CD
- Your team is small-to-medium sized
- You want fast setup with YAML config

**Choose Jenkins when:**
- You need **full control** of your CI/CD infrastructure
- You have **complex, custom pipeline requirements**
- You work in an **enterprise on-premise environment**
- You need integration with many internal tools via plugins

---

## 15. Common Interview Questions & Answers

### Q: What is the difference between `git merge` and `git rebase`?

**Answer:**
- `git merge` combines two branches and creates a **merge commit** — preserves full history, safe for shared branches
- `git rebase` moves or replays commits from one branch on top of another — creates **linear history** but rewrites commits

```bash
# Merge — creates a merge commit, history shows both branches
git checkout main
git merge feature/my-pipeline

# Rebase — replays feature commits on top of main
git checkout feature/my-pipeline
git rebase main
```

> **Rule of thumb:** Never rebase shared/public branches — only rebase your local feature branch.

---

### Q: What is `git stash` and when would you use it?

**Answer:**
`git stash` temporarily saves uncommitted changes so you can switch branches without committing incomplete work.

```bash
# Save current changes
git stash

# List stashes
git stash list

# Apply most recent stash
git stash pop

# Apply without removing from stash list
git stash apply

# Stash with a message
git stash push -m "WIP: aurora connector changes"
```

Use case: You are mid-way through a feature and need to urgently fix a bug on main — stash your work, fix the bug, then pop your stash.

---

### Q: How do you handle secrets and credentials in a CI/CD pipeline?

**Answer:**
Never hardcode credentials in code or config files. Best practices:

1. **GitHub Secrets** — store credentials in GitHub repository settings, reference as `${{ secrets.MY_SECRET }}`
2. **Jenkins Credentials** — use Jenkins Credentials plugin, reference in Jenkinsfile with `credentials('my-cred-id')`
3. **AWS Secrets Manager / HashiCorp Vault** — fetch secrets at runtime
4. **Environment variables** — inject at runtime, never commit to repo
5. **.gitignore** — always ignore `.env` files and credential files

```bash
# .gitignore — always include these
.env
*.pem
profiles.yml          # dbt profiles with passwords
secrets.json
config/credentials/
```

---

### Q: What is the difference between `git fetch` and `git pull`?

**Answer:**
- `git fetch` — downloads changes from remote but **does not merge** them into your local branch. Safe — lets you review before merging.
- `git pull` — fetches **and immediately merges** into your current branch. Equivalent to `git fetch` + `git merge`.

```bash
# Fetch — inspect before merging
git fetch origin
git diff main origin/main     # See what changed
git merge origin/main         # Merge when ready

# Pull — fetch + merge in one step
git pull origin main
```

---

### Q: How would you set up a CI/CD pipeline for a dbt project?

**Answer:**

```
Code pushed to feature branch
        ↓
CI Triggers:
  1. pip install dbt
  2. dbt compile       ← validate models parse correctly
  3. dbt test --select state:modified   ← run tests on changed models
  4. sqlfluff lint     ← SQL style check
        ↓
PR opened → CI results posted to PR
        ↓
Code reviewed + approved
        ↓
Merged to main
        ↓
CD Triggers:
  1. dbt run --target staging
  2. dbt test --target staging
  3. If passes → dbt run --target production
  4. Notify team on Slack
```

---

### Q: What is a webhook and how does GitHub use it with Jenkins?

**Answer:**
A **webhook** is an HTTP callback — GitHub sends a POST request to a specified URL when an event occurs (push, PR open, merge).

Jenkins exposes a webhook endpoint. When GitHub pushes code, it notifies Jenkins, which then triggers the pipeline automatically.

```
Developer pushes code to GitHub
        ↓
GitHub sends POST request to:
http://jenkins-server:8080/github-webhook/
        ↓
Jenkins receives webhook
        ↓
Jenkins triggers the relevant pipeline job
```

Setup:
1. In GitHub repo → Settings → Webhooks → Add webhook
2. Enter Jenkins URL: `http://your-jenkins/github-webhook/`
3. Select events: Push, Pull Request
4. In Jenkins job → Build Triggers → Check "GitHub hook trigger for GITScm polling"

---

## 📌 Key Concepts Summary

| Concept | Description |
|---|---|
| **Git** | Distributed version control system |
| **Repository** | Project directory tracked by Git |
| **Commit** | Snapshot of changes at a point in time |
| **Branch** | Isolated line of development |
| **Merge** | Combine two branches — preserves history |
| **Rebase** | Replay commits on top of another branch — linear history |
| **Pull Request** | Propose, review, and merge code via GitHub |
| **GitFlow** | Structured branching model with develop + release branches |
| **Trunk-Based Dev** | Short-lived branches merged to main frequently |
| **CI** | Automatically test code on every push |
| **CD** | Automatically deploy after CI passes |
| **Jenkins** | Open-source self-hosted CI/CD automation server |
| **Jenkinsfile** | Pipeline-as-code definition in Groovy |
| **GitHub Actions** | Cloud-native CI/CD built into GitHub |
| **Webhook** | HTTP callback to trigger Jenkins from GitHub events |
| **git stash** | Temporarily shelve uncommitted changes |
| **Branch Protection** | Enforce reviews and CI checks before merging |

---

*Mastering Git workflows and CI/CD pipelines is a key differentiator in Data Engineering interviews — it shows you build production-grade, collaborative, and reliable data systems.*