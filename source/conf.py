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

nbsphinx_prolog = """
{%- set docname = env.doc2path(env.docname, base=False) -%}
{%- set github = "yoshanuikabundi/openmm-cookbook/blob/main/" ~ docname -%}
.. raw:: html

    <div class="nbsphinx-prolog">
        <a href="{{ docname }}">Download notebook</a>
        <a href="https://github.com/{{ github }}">View in GitHub</a>
        <a href="https://colab.research.google.com/github/{{ github }}">Open in Google Colab</a>
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
