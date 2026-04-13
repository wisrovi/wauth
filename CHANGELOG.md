# WAuth Changelog

All notable changes to WAuth will be documented in this file.

---

## [Unreleased]

### Added
- **examples/17 pipeline/**: New example demonstrating WAuth + WPipe integration for access control
- **.readthedocs.yaml**: ReadTheDocs configuration file

### Changed
- **pyproject.toml**: Added `furo` theme to docs dependencies
- **docs/index.rst**: Added cross-references to WPipe, badges with cache-busting
- **docs/conf.py**: Fixed `html_baseurl` to `wauth.readthedocs.io`
- **README.md**: Added WPipe integration section
- **Vault**: Replaced raw `sqlite3` with `wsqlite` (Pydantic-backed ORM)
- **Vault**: Added `SecretModel` Pydantic model for schema definition
- **WAuth class**: Added object-oriented API (`WAuth().set()`, `WAuth().get()`)

### Fixed
- **pyproject.toml**: Updated build targets from old `wpipe` references to `wauth`
- **Example**: Fixed `examples/00 base/example.py` to use the new `WAuth` class API

---

## [1.5.1] - 2026-04-10

### Fixed
- Alert system API compatibility with new `expression` parameter
- Performance comparison example using `get_stats()` instead of deprecated method
- Reduced package size (42MB → 140KB) by excluding heavy examples

---

## [1.5.0] - 2026-04-10

### Added
- **ParallelExecutor**: Execute pipeline steps in parallel (ThreadPoolExecutor/ProcessPoolExecutor)
- **ExecutionMode**: IO_BOUND, CPU_BOUND, SEQUENTIAL
- **DAGScheduler**: Dependency graph management with topological sorting
- **PipelineAsStep**: Use pipelines as steps in other pipelines
- **@step()** decorator: Inline step definition
- **StepRegistry**: Central registry for decorated steps
- **ResourceMonitor**: Track RAM/CPU during execution
- **Exporter**: JSON/CSV export capabilities
- **Type validators**: Input/output validation

---

## [1.0.0] - 2024-04-01

### Added
- **Pipeline**: Core pipeline orchestration
- **Condition**: Conditional branching based on data
- **Retry**: Automatic retry with backoff
- **APIClient**: External API integration
- **SQLite/Wsqlite**: Data persistence
- **Error handling**: Custom exceptions with codes
- **YAML config**: Load configurations from YAML
- **Nested pipelines**: Compose complex workflows
- **Progress tracking**: Rich terminal output
- **Type hints**: Complete type annotations