# openmm-cookbook
Proof-of-concept for the OpenMM Cookbook.

Preview at https://yoshanuikabundi.github.io/openmm-cookbook

## Adding a notebook

Notebooks can be added to the cookbook by adding it to the `notebooks` folder. Links to download the notebook, view it in GitHub, or open it in Google Colab are added to the rendered notebook on the website automatically.

"Open in Google Colab" links to a copy of the notebook that is constructed when the documentation is built. This copy has a cell injected that allows the notebook's dependencies to be installed automatically. By default, each notebook will install the Conda Forge packages specified in the `default_conda_forge_deps` variable in `source/conf.py`, and then download all the files in the `default_required_files` variable into the notebook's execution environment. This can be configured on a per-notebook basis by adding the `conda_forge_dependencies` or `required_files` metadata entries to the notebook.

## Releases

The cookbook's `main` branch is intended for use with the latest release of OpenMM. When new cookbooks are added, they will be served immediately and tested against the current release. Nightly tests are performed against OpenMM's development branch, and any fixes required will live in feature branches or a `next` branch. When a new release of OpenMM is cut, the state of `main`, which reflects an entire release cycle, is memorialized with a release tag and rendered to gh-pages in its own release folder. Any feature branches or `next` branches are then merged in so that `main` is now compatible with the new release.

This strategy allows cookbooks for the current version to be released instantly while still permitting testing of notebooks in CI, and preserving the state of the cookbook at each release for posterity.
