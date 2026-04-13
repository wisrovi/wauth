# WAuth Documentation

Professional Sphinx-based documentation for the WAuth library.

## Structure

| File | Description |
|------|-------------|
| [`conf.py`](conf.py) | Sphinx configuration (Furo theme, autodoc, napoleon) |
| [`index.rst`](index.rst) | Main documentation entry point with grid navigation |
| [`getting-started.rst`](getting-started.rst) | Installation and first-use guide |
| [`api.rst`](api.rst) | Complete API reference (autodoc-generated) |
| [`tutorials.rst`](tutorials.rst) | Step-by-step usage guides |
| [`faq.rst`](faq.rst) | Frequently asked questions |
| [`resources.rst`](resources.rst) | Bibliography and external resources |

## Building Documentation

```bash
# Build HTML documentation
make html

# Build and serve locally (opens browser)
make serve
# Then visit http://localhost:8000

# Clean documentation artifacts
make doc-clean
```

## Configuration

- **Theme**: Furo (modern, responsive)
- **Extensions**: autodoc, napoleon (Google Style), sphinx_copybutton, myst_parser, sphinx_design, sphinx_sitemap
- **Author**: William Rodríguez — [LinkedIn](https://es.linkedin.com/in/wisrovi-rodriguez)
- **Language**: English (technical)

## Output

Built documentation is available at `docs/_build/html/index.html`.
