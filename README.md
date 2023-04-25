# openmm-cookbook

This repo is home to the OpenMM Cookbook and the OpenMM Tutorials

The latest release can be viewed here: https://openmm.github.io/openmm-cookbook

The main branch of this repo can be viewed on the development version: https://openmm.github.io/openmm-cookbook/dev/

## Adding a notebook

To add a new cookbook add the ipynb notebook to the `notebooks/cookbook` folder and add a link to it in `cookbook.md`. To add a new tutorial add the ipynb notebook to the `notebooks/tutorials` folder and add a link to it in `tutorials.md`

Links to download the notebook, view it in GitHub, or open it in Google Colab are added to the rendered notebook on the website automatically. Any files required by the notebook should be placed in the same folder as the notebook --- they are required by both the testing apparatus and Google Colab. The notebook must also be added to `index.md`.

"Open in Google Colab" links to a copy of the notebook that is constructed when the documentation is built. This copy has a cell injected that allows the notebook's dependencies to be installed automatically. By default, each notebook will install the Conda Forge packages specified in the `cookbook_default_conda_forge_deps` variable in `conf.py`, and then download all the files in the notebook's folder into the notebook's execution environment. This can be configured on a per-notebook basis by adding the `conda_forge_dependencies` or `required_files` metadata entries to the notebook.

Notebook thumbnails can be configured in several ways, as described in the [nbsphinx documentation](https://nbsphinx.readthedocs.io/).


## Building locally

First clone this repo, then create a conda environment using [environment.yml](environment.yml).
The cookbook can then be built using
```
make html
```
the created html will be in the `build/html` directory and can be viewed by opening `build/html/index.html` in a browser.

## Releases

The cookbooks main branch is the development channel, it is rendered as `https://openmm.github.io/openmm-cookbook/dev/`, anytime the main branch is updated the rendered cookbook will be updated.

When a release is cut the current working state of the cookbook will be preserved as `https://openmm.github.io/openmm-cookbook/refs/tags/${release}/index.html` where `${release}` is the release tag. e.g. `https://openmm.github.io/openmm-cookbook/refs/tags/v0.1/index.html`.
 
 
 The latest version of the cookbook will point to the most recent release `https://openmm.github.io/openmm-cookbook/latest/`

## CI

Continuous integration is run on the main branch of the cookbook. Just the notebooks in `notebooks/cookbook` are run through the CI, tutorials are not (due to long compute time). There are two workflows: [Main](.github/workflows/ci-main.yml) will test that the notebooks run with the latest release of OpenMM, [Nightly](.github/workflows/ci-nightly.yml) will test that the notebooks run with the development version of OpenMM.

## Pull Requests

When a PR is triggered the cookbook will be rendered as `https://openmm.github.io/openmm-cookbook/PR#/` where PR# is the pull request number e.g. [PR16](https://openmm.github.io/openmm-cookbook/PR16/index.html). **Note** that due to github actions permissions the *Deploy to GitHub Pages* step in the [gh-pages workflow](.github/workflows/gh-pages.yml) will only work correctly if the PR comes from a branch *within* `https://github.com/openmm/openmm-cookbook` and it will not work when the PR comes from a personal fork.




