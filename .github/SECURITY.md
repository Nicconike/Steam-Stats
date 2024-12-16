# Security Policy

## Reporting a Vulnerability

Thank you for improving the security of the project. I take security vulnerabilities seriously and appreciate your efforts to responsibly disclose any issues you find.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them to me by following the steps below:

1. **Email**: Send an email to **github.flavorful732@passinbox.com** with the subject "Security Vulnerability Report: Steam-Stats".
2. **Discord**: If you do not prefer the email method, then please reach out to me via [Discord](https://discord.com/) @nicconike, @Nicco#1741 or the [Discord Server](https://discord.gg/UbetHfu)
3. **Open PGP Key**: If possible, encrypt your message with my GPG key. You can download the GPG key from [here](https://keyserver.ubuntu.com/).
4. **Information to Include**:
    - Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
    - Full paths of source file(s) related to the manifestation of the issue
    - The location of the affected source code (tag/branch/commit or direct URL)
    - Any special configuration required to reproduce the issue
    - Step-by-step instructions to reproduce the issue
    - Proof-of-concept or exploit code (if possible)
    - Impact of the issue, including how an attacker might exploit the issue

### How to Use GPG (Open PGP) Key

1. **Download and install GPG software**:
	- **Windows**: [Gpg4win](https://gpg4win.org/)
	- **macOS**: [GPGTools](https://gpgtools.org/)
	- **Linux**: GnuPG (often pre-installed)

2. **Download the public key from the Key Server**:
	1. Open the [OpenPGP server](https://keyserver.ubuntu.com/) website in your browser
	2. Search the key using this fingerprint - `333675FF949C2CDDB86DBD64C82BDEDDEFDE338B`
	3. Now click on the public key which will download the pub key file `333675ff949c2cddb86dbd64c82bdeddefde338b.asc`
		```sh
		rsa4096/333675ff949c2cddb86dbd64c82bdeddefde338b
		```
	4. Please rename the file to something more simpler like `public_key.asc`

3. **Import the public key**:
	- After downloading the public key file (`public_key.asc`), import it into your GPG keyring using the following command:
    	```sh
     	gpg --import public_key.asc
     	```

4. **Verify the imported key**:
	- List the keys in your keyring to verify that the public key has been imported correctly:
     	```sh
     	gpg --list-keys
     	```

5. **Encrypt your message**:
	- Create a text file containing your vulnerability report (e.g., `vulnerability_report.txt`).
	- Encrypt the file using the public key:
    	```sh
     	gpg --encrypt --armor --recipient your.email@example.com vulnerability_report.txt
     	```
	- This will create an encrypted file (e.g., `vulnerability_report.txt.asc`).

6. **Send the encrypted message**:
	- Share the encrypted file (`vulnerability_report.txt.asc`) to me via Discord [@nicconike] or the [Discord Server](https://discord.gg/UbetHfu)

You should receive a response within 24 hours. If for some reason you do not, please follow up via discord to ensure I received your original message.

## Preferred Languages

I would prefer all the communications to be in English.

## Policy

This Project follows the principle of [Coordinated Vulnerability Disclosure](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/about-coordinated-disclosure-of-security-vulnerabilities).

Please see the docs of how to [Privately reporting a security vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| > 1.1.0 | :white_check_mark: |
| < 1.0.2 | :x:                |

Thank you for helping to keep the project **secure!**
