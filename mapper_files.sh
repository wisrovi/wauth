#!/bin/bash
set -e
echo "=== Granular commits starting ==="

# Core library
git add "wauth/__init__.py" && git commit -m "[FEATURE] Add main WAuth class and functional API"
git add "wauth/core.py" && git commit -m "[FEATURE] Add CryptoEngine for Fernet encryption"
git add "wauth/vault.py" && git commit -m "[FEATURE] Add Vault with SQLite persistence"
git add "wauth/utils.py" && git commit -m "[FEATURE] Add machine ID detection utilities"
git add "wauth/exceptions.py" && git commit -m "[FEATURE] Add exception hierarchy (6 exceptions)"
git add "wauth/deprecation.py" && git commit -m "[FEATURE] Add deprecation decorator utilities"
git add "wauth/_log.py" && git commit -m "[FEATURE] Add loguru logging integration"

# Drivers
git add "wauth/drivers/__init__.py" && git commit -m "[FEATURE] Add DriverFactory"
git add "wauth/drivers/local.py" && git commit -m "[FEATURE] Add LocalDriver for encrypted storage"
git add "wauth/drivers/docker.py" && git commit -m "[FEATURE] Add DockerDriver for container secrets"
git add "wauth/drivers/README.md" && git commit -m "[DOC] Add drivers README"
git add "wauth/README.md" && git commit -m "[DOC] Add wauth package README"

# Tests
git add "test/conftest.py" && git commit -m "[TEST] Add pytest fixtures"
git add "test/test_core.py" && git commit -m "[TEST] Add CryptoEngine tests"
git add "test/test_vault.py" && git commit -m "[TEST] Add Vault tests"
git add "test/test_utils.py" && git commit -m "[TEST] Add utilities tests"
git add "test/test_drivers.py" && git commit -m "[TEST] Add drivers tests"
git add "test/test_wauth.py" && git commit -m "[TEST] Add WAuth API tests"
git add "test/test_exceptions.py" && git commit -m "[TEST] Add exception tests"
git add "test/test_deprecation.py" && git commit -m "[TEST] Add deprecation tests"
git add "test/test_log.py" && git commit -m "[TEST] Add logging tests"
git add "test/__init__.py" && git commit -m "[TEST] Add test package init"
git add "test/README.md" && git commit -m "[DOC] Add test README"

# Examples
git add "examples/00 base/example.py" && git commit -m "[FEATURE] Add basic usage example"
git add "examples/01 file storage/example.py" && git commit -m "[FEATURE] Add file storage example"
git add "examples/02 TTL expiration/example.py" && git commit -m "[FEATURE] Add TTL expiration example"
git add "examples/03 key rotation/example.py" && git commit -m "[FEATURE] Add key rotation example"
git add "examples/04 backup and restore/example.py" && git commit -m "[FEATURE] Add backup restore example"
git add "examples/05 async API/example.py" && git commit -m "[FEATURE] Add async API example"
git add "examples/06 exception handling/example.py" && git commit -m "[FEATURE] Add exception handling example"
git add "examples/07 functional API/example.py" && git commit -m "[FEATURE] Add functional API example"
git add "examples/08 Docker secrets/example.py" && git commit -m "[FEATURE] Add Docker secrets example"
git add "examples/09 config file/example.py" && git commit -m "[FEATURE] Add config file example"
git add "examples/10 logging integration/example.py" && git commit -m "[FEATURE] Add logging example"
git add "examples/11 migration from env/example.py" && git commit -m "[FEATURE] Add migration example"
git add "examples/12 multiple vaults/example.py" && git commit -m "[FEATURE] Add multiple vaults example"
git add "examples/13 security best practices/example.py" && git commit -m "[FEATURE] Add security best practices example"
git add "examples/14 web app integration/example.py" && git commit -m "[FEATURE] Add web app integration example"
git add "examples/15 CI-CD pipeline/example.py" && git commit -m "[FEATURE] Add CI-CD pipeline example"
git add "examples/16 bulk operations/example.py" && git commit -m "[FEATURE] Add bulk operations example"
git add "examples/README.md" && git commit -m "[DOC] Add examples README"
git add "examples/00 base/README.md" && git commit -m "[DOC] Add example 00 README"
git add "examples/00 base/wauth.db" && git commit -m "[CONFIG] Add example database"
git add "examples/00 base/wauth2.db" && git commit -m "[CONFIG] Add example database v2"

# Benchmarks
git add "benchmarks/performance.py" && git commit -m "[FEATURE] Add performance benchmarks"
git add "benchmarks/README.md" && git commit -m "[DOC] Add benchmarks README"

# Technical Whitepaper
git add "docs/main.tex" && git commit -m "[DOC] Add technical whitepaper LaTeX source"
git add "docs/main.pdf" && git commit -m "[DOC] Add technical whitepaper PDF (60 pages)"

# Diagrams
git add "docs/sources/01-ecosystem-context.mmd" && git commit -m "[DOC] Add ecosystem context diagram source"
git add "docs/sources/01-ecosystem-context.png" && git commit -m "[DOC] Add ecosystem context diagram PNG"
git add "docs/sources/02-core-logic-flow.mmd" && git commit -m "[DOC] Add core logic flow diagram source"
git add "docs/sources/02-core-logic-flow.png" && git commit -m "[DOC] Add core logic flow diagram PNG"
git add "docs/sources/03-structural-component-map.mmd" && git commit -m "[DOC] Add structural component map diagram source"
git add "docs/sources/03-structural-component-map.png" && git commit -m "[DOC] Add structural component diagram PNG"
git add "docs/sources/04-sequence-interaction-set.mmd" && git commit -m "[DOC] Add sequence set diagram source"
git add "docs/sources/04-sequence-interaction-set.png" && git commit -m "[DOC] Add sequence set diagram PNG"
git add "docs/sources/05-sequence-interaction-get.mmd" && git commit -m "[DOC] Add sequence get diagram source"
git add "docs/sources/05-sequence-interaction-get.png" && git commit -m "[DOC] Add sequence get diagram PNG"
git add "docs/sources/06-application-lifecycle.mmd" && git commit -m "[DOC] Add application lifecycle diagram source"
git add "docs/sources/06-application-lifecycle.png" && git commit -m "[DOC] Add application lifecycle PNG"
git add "docs/sources/07-infrastructure-topology.mmd" && git commit -m "[DOC] Add infrastructure topology diagram source"
git add "docs/sources/07-infrastructure-topology.png" && git commit -m "[DOC] Add infrastructure topology PNG"
git add "docs/sources/08-data-mutation-map.mmd" && git commit -m "[DOC] Add data mutation map diagram source"
git add "docs/sources/08-data-mutation-map.png" && git commit -m "[DOC] Add data mutation map PNG"
git add "docs/sources/09-security-hardening-layers.mmd" && git commit -m "[DOC] Add security layers diagram source"
git add "docs/sources/09-security-hardening-layers.png" && git commit -m "[DOC] Add security layers PNG"
git add "docs/sources/10-error-recovery-flow.mmd" && git commit -m "[DOC] Add error recovery flow diagram source"
git add "docs/sources/10-error-recovery-flow.png" && git commit -m "[DOC] Add error recovery flow PNG"
git add "docs/sources/11-deployment-pipeline.mmd" && git commit -m "[DOC] Add deployment pipeline diagram source"
git add "docs/sources/11-deployment-pipeline.png" && git commit -m "[DOC] Add deployment pipeline PNG"

# Docs infrastructure
git add "docs/README.md" && git commit -m "[DOC] Add docs README"
git add "docs/conf.py" && git commit -m "[CONFIG] Add Sphinx conf"
git add "docs/index.rst" && git commit -m "[DOC] Add docs index"
git add "docs/api.rst" && git commit -m "[DOC] Add API docs"
git add "docs/getting-started.rst" && git commit -m "[DOC] Add getting started docs"
git add "docs/tutorials.rst" && git commit -m "[DOC] Add tutorials"
git add "docs/faq.rst" && git commit -m "[DOC] Add FAQ docs"
git add "docs/resources.rst" && git commit -m "[DOC] Add resources docs"
git add "docs/source/wauth.rst" && git commit -m "[DOC] Add wauth RST"
git add "docs/source/wauth.core.rst" && git commit -m "[DOC] Add wauth.core RST"
git add "docs/source/wauth.drivers.rst" && git commit -m "[DOC] Add wauth.drivers RST"
git add "docs/source/wauth.drivers.local.rst" && git commit -m "[DOC] Add wauth.drivers.local RST"
git add "docs/source/wauth.drivers.docker.rst" && git commit -m "[DOC] Add wauth.drivers.docker RST"
git add "docs/source/wauth.exceptions.rst" && git commit -m "[DOC] Add wauth.exceptions RST"
git add "docs/source/wauth.utils.rst" && git commit -m "[DOC] Add wauth.utils RST"
git add "docs/source/wauth.vault.rst" && git commit -m "[DOC] Add wauth.vault RST"
git add "docs/source/wauth.deprecation.rst" && git commit -m "[DOC] Add wauth.deprecation RST"
git add "docs/source/modules.rst" && git commit -m "[DOC] Add modules RST"

# Config files
git add "Makefile" && git commit -m "[CONFIG] Add Makefile"
git add "pyproject.toml" && git commit -m "[CONFIG] Update pyproject.toml"
git add "README.md" && git commit -m "[DOC] Update README"
git add "CHANGELOG.md" && git commit -m "[DOC] Update CHANGELOG"
git add "MIGRATION.md" && git commit -m "[DOC] Add migration guide"
git add "VERSIONING.md" && git commit -m "[DOC] Add versioning policy"
git add "SECURITY.md" && git commit -m "[DOC] Add security policy"
git add "PYLINT_REPORT.md" && git commit -m "[DOC] Add Pylint report"

# Extra outputs
git add "wauth-technical-whitepaper.pdf" && git commit -m "[DOC] Add technical whitepaper PDF (root copy)"
git add "opencode_history.md" && git commit -m "[DOC] Add opencode history"

# Databases
git add "wauth.db" && git commit -m "[CONFIG] Add database"
git add "wauth2.db" && git commit -m "[CONFIG] Add database v2"
git add "puppeteer-config.json" && git commit -m "[CONFIG] Add puppeteer config"

# Qwen settings
git add ".qwen/settings.json" && git commit -m "[CONFIG] Add qwen settings"

# Git mapper script
git add "mapper_files.sh" && git commit -m "[CONFIG] Add git mapper script"

# Deleted files
git add "enviroment/.gitkeep" "examples/module/.gitkeep" "module/__init__.py" "module/submodule/__init__.py" "module/submodule/controller.py" && git commit -m "[FIX] Remove deprecated module directory"

echo "=== Done (100+ commits) ==="