# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = "openmm-cookbook"
copyright = "2021, The OpenMM Contributors"
author = "The OpenMM Contributors"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "nbsphinx",
]

# Links to the OpenMM docs
intersphinx_mapping = {
    "openmm": ("http://docs.openmm.org/latest/api-python/", None),
    "userguide": ("http://docs.openmm.org/latest/userguide/", None),
    "devguide": ("http://docs.openmm.org/latest/developerguide/", None),
}

# nbsphinx config

# Set up colab-compatible notebooks
import json
from pathlib import Path
from uuid import uuid4
from subprocess import run

build_colab = Path("../build/html/colab")
build_colab.mkdir(parents=True, exist_ok=True)

notebooks_path = Path("notebooks")

default_conda_forge_deps = [
    "openmm",
]
default_required_files = [
    "notebooks/ala_ala_ala.pdb",
    "villin.pdb",
]

for fn in notebooks_path.glob("*.ipynb"):
    notebook_json = fn.read_text()
    notebook = json.loads(notebook_json)
    conda_deps = notebook["metadata"].get(
        "conda_forge_dependencies", default_conda_forge_deps
    )
    file_deps = notebook["metadata"].get("required_files", default_required_files)
    wgets = [
        f"!wget -q 'https://raw.githubusercontent.com/Yoshanuikabundi/openmm-cookbook/main/{dep}'\n"
        for dep in file_deps
    ]
    if wgets:
        wgets = [
            "# We also need to get a few files that the cookbook depends on\n"
        ] + wgets
    cell = {
        "cell_type": "code",
        "execution_count": 0,
        "id": str(uuid4()),
        "metadata": {},
        "outputs": [],
        "source": [
            "# Execute this cell to install OpenMM in the Colab environment\n",
            "!pip install -q condacolab\n",
            "import condacolab\n",
            "condacolab.install_mambaforge()\n",
            f"!mamba install {' '.join(conda_deps)}\n",
            *wgets,
        ],
    }
    notebook["cells"].insert(0, cell)
    fn_out = build_colab / fn
    fn_out.parent.mkdir(parents=True, exist_ok=True)
    with fn_out.open("w") as file:
        json.dump(notebook, file)

# Add links to top of each notebook
nbsphinx_prolog = """
{%- set docname = env.doc2path(env.docname, base=False) -%}
{%- set github = "yoshanuikabundi/openmm-cookbook" -%}
{%- set on_local = docname.split('/') | last -%}
{%- set on_github = "https://github.com/" ~ github ~ "/blob/main/" ~ docname -%}
{%- set on_colab = "https://colab.research.google.com/github/" ~ github ~ "/blob/gh-pages/dev/colab/" ~ docname -%}
.. raw:: html

    <div class="nbsphinx-prolog">
        <a href="{{ on_local }}">Download notebook</a>
        <a href="{{ on_github }}">View in GitHub</a>
        <a href="{{ on_colab }}">Open in Google Colab</a>
    </div>

"""

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
pygments_style = "sphinx"

html_theme = "alabaster"
html_theme_options = {
    "github_button": False,
    "github_user": "openmm",
    "github_repo": "openmm-cookbook",
    "logo_name": True,
    "logo": "logo.png",
    "extra_nav_links": [
        {
            "title": "OpenMM.org",
            "uri": "https://openmm.org",
            "relative": False,
        },
        {
            "title": "User's Manual",
            "uri": "http://docs.openmm.org/latest/userguide/",
            "relative": False,
        },
        {
            "title": "Developer Guide",
            "uri": "http://docs.openmm.org/latest/developerguide/",
            "relative": False,
        },
        {
            "title": "C++ API reference",
            "uri": "http://docs.openmm.org/latest/api-c++/",
            "relative": False,
        },
        {
            "title": "Python API reference",
            "uri": "http://docs.openmm.org/latest/api-python/",
            "relative": False,
        },
        {
            "title": "GitHub",
            "uri": "https://github.com/openmm",
            "relative": False,
        },
    ],
    "show_relbar_bottom": True,
}
html_sidebars = {
    "**": [
        "about.html",
        "searchbox.html",
        "navigation.html",
    ]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "notebooks.css",
]
