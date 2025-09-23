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
import os
import sys

sys.path.insert(0, os.path.abspath("./sphinx"))

# -- Project information -----------------------------------------------------

project = "OpenMM Cookbook & Tutorials"
copyright = "2025, The OpenMM Contributors"
author = "The OpenMM Contributors"
release = os.getenv("PAGES_DEPLOY_PATH","dev")
print(release)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "nbsphinx",
    "cookbook",
]

# Links to the OpenMM docs
intersphinx_mapping = {
    "openmm": ("https://docs.openmm.org/latest/api-python/", None),
    "userguide": ("https://docs.openmm.org/latest/userguide/", None),
    "devguide": ("https://docs.openmm.org/latest/developerguide/", None),
}

cookbook_default_pypi_deps = ["openmm"]
cookbook_required_files_base_uri = (
    "https://raw.githubusercontent.com/openmm/openmm-cookbook/main"
)

### nbsphinx config ###

# Add links to top of each notebook
nbsphinx_prolog = """
{%- set colabpath = env.config.release -%}
{%- set docname = env.doc2path(env.docname, base=False) -%}
{%- set github = "openmm/openmm-cookbook" -%}
{%- set on_local = docname.split('/') | last -%}
{%- set on_github = "https://github.com/" ~ github ~ "/blob/main/" ~ docname -%}
{%- set on_colab = "https://colab.research.google.com/github/" ~ github ~ "/blob/gh-pages/" ~ colabpath ~ "/colab/" ~ docname -%}
.. raw:: html

    <div class="nbsphinx-prolog">
        <a href="{{ on_local }}">Download Notebook</a>
        <a href="{{ on_github }}">View in GitHub</a>
        <a href="{{ on_colab }}">Open in Google Colab</a>
    </div>

"""

# Add any paths that contain templates here, relative to this directory.
templates_path = ["sphinx/_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "README.md",
    "**/README.md",
    "build",
    "sphinx",
    ".*",
    "**/.*",
]

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
    "logo": "logo.svg",
    "extra_nav_links": [
        {
            "title": "OpenMM.org",
            "uri": "https://openmm.org",
            "relative": False,
        },
        {
            "title": "User's Manual",
            "uri": "https://docs.openmm.org/latest/userguide/",
            "relative": False,
        },
        {
            "title": "Developer Guide",
            "uri": "https://docs.openmm.org/latest/developerguide/",
            "relative": False,
        },
        {
            "title": "C++ API reference",
            "uri": "https://docs.openmm.org/latest/api-c++/",
            "relative": False,
        },
        {
            "title": "Python API reference",
            "uri": "https://docs.openmm.org/latest/api-python/",
            "relative": False,
        },
        {
            "title": "GitHub",
            "uri": "https://github.com/openmm/openmm",
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
html_static_path = ["sphinx/_static"]

html_css_files = [
    "notebooks.css",
]
