# Security Policy

## 👤 About This Project

Steam Stats is **maintained by a single developer** (@nicconike) as an open-source GitHub Action. This security policy reflects the realities of solo project maintenance while maintaining security best practices.

## 🔒 Security Standards & Compliance

### OpenSSF Scorecard
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9965/badge)](https://www.bestpractices.dev/projects/9965)

**Steam Stats** best practices and maintains high security standards:

- ✅ **Pinned Dependencies** - All dependencies are pinned to specific versions
- ✅ **Code Review Required** - All changes require peer review before merging
- ✅ **Automated Security Scanning** - Continuous security analysis via GitHub Security features
- ✅ **SAST Analysis** - Static Application Security Testing with CodeQL
- ✅ **Dependency Scanning** - Automated vulnerability detection in dependencies
- ✅ **Secret Scanning** - Prevention of credential exposure
- ✅ **Container Security** - Secure Docker image builds and scanning

### Security Measures Implemented

| Security Control | Implementation | Status |
|-----------------|----------------|---------|
| **Code Analysis** | CodeQL, Bandit, Pylint (10.0/10), SonarQube | ✅ Active |
| **Dependency Management** | Dependabot, Dependency Review | ✅ Active |
| **Secret Protection** | GitHub Secret Scanning, Pre-commit hooks | ✅ Active |
| **Container Security** | Multi-stage builds, Non-root user | ✅ Active |
| **Infrastructure Security** | Step Security Harden Runner | ✅ Active |
| **Access Control** | Branch protection, Required reviews | ✅ Active |

## 🚨 Reporting Security Vulnerabilities

**⚠️ IMPORTANT: Please do not report security vulnerabilities through public GitHub issues, discussions or pull requests.**

### Primary Reporting Methods

#### 1. **GitHub Private Security Advisory (Preferred)**
Use GitHub's private vulnerability reporting:
- Go to the [Security tab](https://github.com/Nicconike/Steam-Stats/security)
- Click **"Report a vulnerability"**
- Fill out the private advisory form
- Secure, built-in, trackable

#### 2. **Email** (Alternative)
Send detailed vulnerability reports to: **github.giving328@passmail.com**
- Subject: `[SECURITY] Steam-Stats Vulnerability Report`
- Use PGP encryption (optional but recommended)

#### 3. **Discord**
For urgent issues or if email is unavailable:
- Discord: **@nicconike** or **@Nicco#1741**
- [Discord Server](https://discord.gg/UbetHfu)

### 🔐 PGP Encryption *(Optional)*

For sensitive reports, you can encrypt your message using my PGP key:

- **PGP Fingerprint:** `FAF455A3287AAF52858D8A097217AE9924885496`
- **Key Servers:** keyserver.ubuntu.com, keys.openpgp.org

#### Quick PGP Setup:
1. **Download Key:**
   ```bash
   curl -s https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xFAF455A3287AAF52858D8A097217AE9924885496 | gpg --import
   ```

2. **Encrypt Your Report:**
   ```bash
   echo "Your vulnerability report here" | gpg --encrypt --armor --recipient FAF455A3287AAF52858D8A097217AE9924885496
   ```

3. **Send encrypted content via email or Discord**

### 📝 Information to Include

To help me understand and reproduce the issue, please include:

#### Required Information:
- **Vulnerability Type** (e.g., RCE, XSS, injection, privilege escalation, API Abuse)
- **Affected Component/Version** (specific commit SHA, version or branch)
- **Attack Vector** (local, network, adjacent network, physical)
- **Impact Assessment** (confidentiality, integrity, availability impact)

#### Helpful Details:
- **Reproduction Steps** (detailed, step-by-step instructions)
- **Proof of Concept** (code, screenshots or demo video)
- **Suggested Fix** (if you have recommendations)
- **Affected Configurations** (specific setups where vulnerability applies)

#### Example Report Template:
```md
**Vulnerability Type:** [e.g., Container Escape, Code Injection]
**Affected Component:** [e.g., api/main.py, Dockerfile, GitHub Actions]
**Severity Assessment:** [Critical/High/Medium/Low]

**Description:**
[Brief explanation of what the vulnerability allows an attacker to do]

**Impact:**
- What systems/data could be compromised?
- Is this exploitable in typical usage scenarios?

**Reproduction Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Proof of Concept:**
[Code snippet, commands or screenshots demonstrating the issue]

**Suggested Mitigation:**
[If you have recommendations for fixes]
```

## ⏰ Response Process (Solo Maintainer)

### Realistic Timeline

| Step                  |  Timeframe      |  What Happens |
|-----------------------|-----------------|-----------------------------------------|
| Acknowledgment        |  48-72 hours    |  I'll confirm I received your report |
| Initial Assessment    |  1-2 weeks      |  I'll reproduce and assess the vulnerability |
| Status Update         |  Every 2 weeks  |  Progress updates during investigation |
| Fix Development       |  2-4 weeks      |  Depends on complexity and my availability |
| Release & Disclosure  |  After fix      |  Public advisory with fix release |

### Response Workflow

1. **📨 Report Received**: Automatic acknowledgment within 48-72 hours
2. **🔍 Validation**: I'll reproduce and assess the issue
3. **📊 Risk Assessment**: Severity scoring using CVSS 4 framework
4. **🛠️ Fix Development**: Patch development and testing
5. **🔒 Security Advisory**: CVE request and coordinated disclosure
6. **🚀 Release**: Security update deployment
7. **📢 Public Disclosure**: Responsible disclosure with credit to reporter

**✅ What I CAN provide:**
- Prompt acknowledgment of reports
- Honest assessment of vulnerabilities
- Timely fixes for confirmed issues
- Public credit to researchers (if desired)
- Transparent communication about progress

**❌ What I CANNOT provide:**
- Bug bounties or financial rewards
- 24/7 response times
- Legal immunity statements
- Formal SLA commitments (realistic timelines only)

### Severity Classification

| Severity | CVSS Score | Response Target | Example |
|----------|------------|----------------|---------|
| **Critical** | 9.0-10.0 | 1-2 weeks | Remote code execution, data breach |
| **High** | 7.0-8.9 | 2-3 weeks | Privilege escalation, authentication bypass |
| **Medium** | 4.0-6.9 | 1 month | Information disclosure, DoS |
| **Low** | 0.1-3.9 | 2-3 months | Minor information leaks, configuration issues |

## 🏆 Security Hall of Fame

### Researchers Who Help Keep Steam Stats Secure

*This section recognizes security researchers who have responsibly disclosed vulnerabilities and helped improve Steam Stats security.*

| Date | Researcher | Vulnerability Type | Severity | Status |
|------|------------|-------------------|----------|---------|
| *None Yet* | - | - | - | - |

### Recognition for Security Researchers

While I cannot offer monetary bounties as a solo developer, security researchers receive:

- 🏅 **Hall of Fame listing** with your preferred name/handle (link to GitHub/website if desired)
- 📜 **Public acknowledgment** in release notes and GitHub security advisories
- 🎯 **Priority support** for any future issues or feature requests
- ⭐ **Social media recognition** (Twitter/X, LinkedIn) if desired
- 🤝 **Direct collaboration opportunities** on security improvements and code review

*Want to be the first researcher in the Hall of Fame? [Report a vulnerability responsibly!](#-reporting-security-vulnerabilities)*

## 🎯 Vulnerability Scope

### **In Scope for Steam Stats:**

**✅ Please report:**
- **Code injection** in Python modules
- **Container escape** vulnerabilities
- **GitHub Actions workflow** security issues
- **Dependency vulnerabilities** not caught by automated scanning
- **Steam API credential exposure** risks
- **Docker image** security issues

**❌ Out of Scope:**
- Issues in **Steam's Web API** itself (report to [Valve](https://www.valvesoftware.com/en/about))
- **User misconfiguration** (document in issues instead)
- **GitHub Actions platform** bugs (report to [GitHub](https://support.github.com/))
- **Theoretical attacks** with no practical impact

### **For GitHub Action Users:**

Since Steam Stats is used as `uses: nicconike/steam-stats@master`, security considerations include:

**User Responsibilities:**
- Secure your own **Steam API keys** and **repository secrets**
- Use **specific version tags** and **pinned versions** instead of `@master` for production (e.g., `@v1.4.0` or `@7d722979930a8521760e200e353382666d0cb483`)
- Review **workflow permissions** and use minimal scopes
- Keep your **GitHub Actions runner** environments secure

**Steam Stats Responsibilities:**
- Maintain secure **Docker container builds**
- Handle **Steam API credentials** securely (never log or expose)
- Provide **security updates** via new releases
- Follow **secure coding practices** in all modules

## 🛡️ Security Architecture

### Threat Model

Steam Stats operates under the following security assumptions:

#### **Assets Protected:**
- User Steam data (API keys, profile information)
- Generated PNG assets
- GitHub repository and CI/CD pipeline
- Docker container runtime environment

#### **Attack Surfaces:**
- Steam Web API integration
- GitHub Actions workflows
- Docker container execution
- Python dependencies and runtime

#### **Threat Actors:**
- Malicious users attempting to extract Steam API keys
- Supply chain attacks via dependencies
- Container escape attempts
- CI/CD pipeline manipulation

### Security Boundaries

```
┌─────────────────────────────────────────────┐
│             GitHub Actions Runner           │
├─────────────────────────────────────────────┤
│  ┌───────────────────────────────────────┐  │
│  │        Docker Container               │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │     Steam Stats Application     │  │  │
│  │  │                                 │  │  │
│  │  │  • Steam API Client             │  │  │
│  │  │  • PNG Generation               │  │  │
│  │  │  • File System Access           │  │  │
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
          │                        │
          ▼                        ▼
   Steam Web API              User Repository
```

## 🔄 Supported Versions

| Version | Support Status | Upgrade Path |
|---------|---------------|------------------|
| **≥ v1.4.0** | ✅ **Full support** | Keep updated with latest releases |
| **v1.3.x** | ⚠️ **Critical fixes only** | Update workflow to use `@v1.4.0` |

### How Users Should Upgrade:

**In your workflow file (`.github/workflows/steam-stats.yml`):**
```yaml
# ❌ Insecure (always latest)
uses: nicconike/steam-stats@master

# ✅ Secure (pinned tag)
uses: nicconike/steam-stats@v1.4.0

# ✅ Secure (pinned commit-SHA)
uses: nicconike/steam-stats@7d722979930a8521760e200e353382666d0cb483
```

**Why pin versions?** Using `@master` pulls the latest code which could include untested changes. **Pinned versions** are tested and stable.

## 🤝 Coordinated Vulnerability Disclosure (CVD)

### **What is CVD?**
**Coordinated Vulnerability Disclosure** means we work **together** to:
1. **Keep the vulnerability private** while developing a fix
2. **Coordinate timing** for public disclosure
3. **Release the fix** before disclosing details publicly
4. **Share credit** with the researcher who found the issue

### **Why CVD for Steam Stats?**
- **Protects users** who haven't updated yet
- **Prevents exploitation** while fixes are being developed
- **Maintains trust** in the open-source ecosystem
- **Standard practice** for responsible open-source projects

### **What You Need to Do (Nothing Extra!)**
As a solo maintainer, CVD just means:
- **Don't publish vulnerability details immediately** when you find them
- **Work with reporters privately** until a fix is ready
- **Release fixes first**, then publish details
- **Give credit** to researchers who help

## 🛡️ Security Measures

### **Automated Security (Already Implemented):**
- ✅ **CodeQL Analysis** - Weekly code security scans
- ✅ **Dependabot** - Automatic dependency vulnerability alerts
- ✅ **Dependency Review** - Blocks PRs with vulnerable dependencies
- ✅ **Bandit Security Scanning** - Python security issue detection
- ✅ **Container Scanning** - Docker image vulnerability checks
- ✅ **OpenSSF Scorecard** - Continuous security posture monitoring

### **Manual Security Practices:**
- ✅ **Pinned dependencies** in pyproject.toml
- ✅ **Minimal permissions** in GitHub Actions workflows
- ✅ **Non-root container execution**
- ✅ **Secret scanning** prevention
- ✅ **Branch protection** with required reviews

## 🔗 Additional Resources

- **GitHub Security Features:** [Repository Security](https://github.com/Nicconike/Steam-Stats/security)
- **OpenSSF Scorecard:** [Detailed Security Metrics](https://scorecard.dev/viewer/?uri=github.com/Nicconike/Steam-Stats)
- **Best Practices Badge:** [CII Best Practices](https://www.bestpractices.dev/projects/9965)

***

## 🤝 Contact & Support

- **Security:** github.giving328@passmail.com
- **General Issues:** [GitHub Issues](https://github.com/Nicconike/Steam-Stats/issues), Tag with `security` label
- **Discussions:** [GitHub Discussions](https://github.com/Nicconike/Steam-Stats/discussions)

**Thank you for helping keep Steam Stats and our community secure! 🙏**

*As a solo maintainer, I appreciate your patience and understanding. Security is important to me, but please keep in mind this is maintained by one person with other commitments.*

***
*Last Updated: October 5, 2025*

*Policy Version: 2.0*
