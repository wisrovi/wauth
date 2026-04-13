# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.6.x (LTS) | ✅ Yes |
| < 1.6 | ❌ No |

## Reporting a Vulnerability

We take the security of WAuth seriously. If you discover a security
vulnerability, please follow these steps:

1. **Do NOT open a public issue** for security vulnerabilities.
2. Email the maint directly: **wisrovi.rodriguez@gmail.com**
3. Include a detailed description of the vulnerability, steps to
   reproduce, and potential impact.
4. You will receive an acknowledgment within **48 hours**.
5. We aim to publish a fix within **30 days** for critical issues.

## Security Architecture

### Encryption

- **Algorithm**: Fernet (AES-128-CBC with HMAC-SHA256 authentication)
- **Key Size**: 32 bytes (256 bits), derived via SHA-256
- **IV**: Random 128-bit IV per encryption operation
- **Key Derivation**: Machine ID + salt → SHA-256 → 32-byte key

### Threat Model

| Threat | Mitigation |
|--------|-----------|
| **Database file theft** | Secrets encrypted — useless without the key |
| **Key exposure** | Key derived from machine ID, not stored in DB |
| **Token tampering** | Fernet's HMAC detects any modification |
| **Brute force** | 256-bit key space makes brute force infeasible |
| **Cross-machine leakage** | Machine-locked keys prevent decryption elsewhere |
| **Docker secret exposure** | Read-only access to `/run/secrets`, no caching |

### Known Limitations

1. **Machine-locked by design**: Secrets encrypted on Machine A cannot
   be decrypted on Machine B. This is intentional, not a bug.
2. **Single key per vault**: All secrets share the same encryption key.
   Key rotation re-encrypts all secrets atomically.
3. **No forward secrecy**: If the key is compromised, all secrets are
   potentially at risk (mitigated by machine-locking).

### Security Audits

| Date | Tool | Result |
|------|------|--------|
| 2026-04-13 | Bandit | 0 Medium/High findings |
| 2026-04-13 | pip-audit | 0 known vulnerabilities |
| 2026-04-13 | Manual review | Architecture reviewed by maintainer |

### Dependencies

All dependencies are monitored via GitHub Actions `pip-audit` and
`safety` workflows. Known vulnerable versions are updated promptly.

### Best Practices for Users

- Use `custom_key` for additional encryption control
- Rotate keys periodically with `auth.rotate_key(new_key)`
- Back up your vault with `auth.backup("path")`
- Never commit `.db` files to version control
- Use Docker secrets for cross-machine deployments

---

**Author:** William Rodríguez — wisrovi  
**LinkedIn:** https://es.linkedin.com/in/wisrovi-rodriguez
