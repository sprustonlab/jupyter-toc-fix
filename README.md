# jupyter-toc-fix

A minimal Python package that automatically configures `jupyter_contrib_nbextensions` with useful extensions and fixes the Table of Contents (TOC2) positioning issue.

## Features

During installation, this package automatically:
1. Installs jupyter_contrib_nbextensions to the environment
2. Enables the nbextensions configurator
3. Activates the following extensions:
   - **toc2** - Table of Contents navigator
   - **collapsible_headings** - Collapse sections by heading
   - **hide_input_all** - Toggle to hide all input cells
   - **init_cell** - Mark cells to run on notebook startup
   - **codefolding** - Fold code sections
4. Applies a CSS fix for TOC positioning bug

## Problem

The TOC2 extension in `jupyter_contrib_nbextensions` has a long-standing CSS positioning bug where the table of contents appears hidden behind the notebook header or positioned off-screen.

## Solution

This package handles all nbextensions setup and applies the CSS fix automatically during pip installation.

## Installation

### From GitHub (recommended for environments)

Add to your conda environment yml file:

```yaml
- pip:
  - git+https://github.com/sprustonlab/jupyter-toc-fix.git
```

Or install directly:

```bash
pip install git+https://github.com/sprustonlab/jupyter-toc-fix.git
```

### Example Environment

See [`example-environment.yml`](example-environment.yml) for a complete Jupyter Notebook 6 environment with:
- Notebook 6.1.4
- All widgets (ipywidgets, anywidget)
- Jupyter extensions auto-configured
- nb_conda_kernels for multi-environment kernel support
- TOC positioning fix applied automatically

### Local installation (for development)

```bash
cd jupyter-toc-fix
pip install -e .
```

## How it works

During installation, the package:
1. Detects the Jupyter configuration directory (respects `JUPYTER_CONFIG_DIR` environment variable)
2. Runs `jupyter contrib nbextension install --sys-prefix`
3. Runs `jupyter nbextensions_configurator enable --sys-prefix`
4. Enables each of the 5 extensions listed above using `--sys-prefix` flag
5. Creates a `custom/custom.css` file if it doesn't exist
6. Appends CSS rules that fix the TOC positioning
7. Works with both conda environments and standard Python installations

## CSS Applied

```css
/* Original Stack Overflow fix - prevents TOC from overlapping with header */
.container {
    width: 70% !important;
    align: left !important;
}

#toc-wrapper {
    position: relative !important;
    width: 20% !important;
    top: 130px !important;
    left: 0px !important;
}
```

**Note:** This is the exact CSS from the Stack Overflow solution. When TOC is docked, the container width ensures code cells don't overlap with it.

## Requirements

- Python >= 3.6
- Jupyter Notebook
- jupyter_contrib_nbextensions (with toc2 extension)

## References

- [Stack Overflow: TOC positioning fix](https://stackoverflow.com/questions/75621836)
- [GitHub Issue: nbextensions TOC compatibility](https://github.com/ipython-contrib/jupyter_contrib_nbextensions/issues/1568)

## License

MIT License

## Author

Spruston Lab
