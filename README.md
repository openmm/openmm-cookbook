# openmm-cookbook
Proof-of-concept for the OpenMM Cookbook.

Preview at https://yoshanuikabundi.github.io/openmm-cookbook

## Adding a notebook

Notebooks can be added to the cookbook by adding it to the `notebooks` folder. Links to download the notebook, view it in GitHub, or open it in Google Colab are added to the rendered notebook on the website automatically.

"Open in Google Colab" links to a copy of the notebook that is constructed when the documentation is built. This copy has a cell injected that allows the notebook's dependencies to be installed automatically. By default, each notebook will install the Conda Forge packages specified in the `default_conda_forge_deps` variable in `source/conf.py`, and then download all the files in the `default_required_files` variable into the notebook's execution environment. This can be configured on a per-notebook basis by adding the `conda_forge_dependencies` or `required_files` metadata entries to the notebook.
