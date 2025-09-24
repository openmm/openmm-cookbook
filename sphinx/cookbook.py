import json
from copy import deepcopy
from docutils.nodes import document
from pathlib import Path
from typing import List, Optional, Any
from uuid import uuid4

from sphinx.application import Sphinx as Application
from sphinx.config import Config
from sphinx.environment import BuildEnvironment


def insert_cell(
    notebook: dict,
    cell_type: str = "code",
    position: int = 0,
    source: Optional[List[str]] = None,
    metadata: Optional[dict] = None,
    outputs: Optional[List[str]] = None,
) -> dict:
    """Insert a cell created from the arguments into a new copy of the notebook

    Args:
        notebook: An ipython/jupyter notebook in dict form. Can be generated
                  by parsing the notebook file as json
        cell_type: The cell type; "code", "markdown", "raw", etc
        position: The position of the new cell in the finished notebook. See dict.insert()
        source: A list of lines of source code for the cell. Newlines are inserted at the
                end of each line in the list
        metadata: A dictionary of metadata values. Should be encodable as json.
        output: A list of lines of text output for the cell. Newlines are inserted at the
                end of each line in the list

    Returns:
        dict: A copy of the input notebook with the cell inserted.
    """
    source = [] if source is None else "\n".join(source).splitlines(keepends=True)
    outputs = [] if outputs is None else "\n".join(outputs).splitlines(keepends=True)
    metadata = {} if metadata is None else metadata
    notebook = deepcopy(notebook)

    cell = {
        "cell_type": cell_type,
        "execution_count": 0,
        "id": str(uuid4()),
        "metadata": metadata,
        "outputs": outputs,
        "source": source,
    }

    notebook.setdefault("cells", []).insert(position, cell)
    return notebook


def get_metadata(
    notebook: dict,
    key: str,
    default,
):
    """Get a notebook's metadata value for a key, or the given default if the key is absent"""
    return notebook.get("metadata", {}).get(key, default)


def create_colab_notebook(notebook, notebook_path: Path, outpath: Path, config: Config):
    """Create a copy of the notebook for Google Colab and save it to output

    The copy will have a cell inserted at the start of the notebook that gathers
    the notebook's dependencies. These dependencies come in two sorts:
     - PyPI dependencies, installed via pip
     - Files, downloaded from the config value `cookbook_required_files_base_uri`

    These dependencies can be specified in the following places. The first value found
    in the following order is used:
    1. In the `pypi_dependencies` or `required_files` metadata fields for an
       individual notebook
    2. In the `cookbook_default_pypi_deps` or `cookbook_default_required_files`
       config values for the entire cookbook
    3. (files only) If the `cookbook_default_required_files` config value is not set,
       all files in the notebook's directory except those with the `.ipynb` file extension
       will be used as dependencies. Set `cookbook_default_required_files` to the empty
       list to specify no dependencies as a default.

    """

    if config.cookbook_default_required_files is None:
        file_list = [
            fn for fn in notebook_path.parent.glob("*.*") if fn.suffix != ".ipynb"
        ]
    else:
        file_list = list(config.cookbook_default_required_files)

    file_deps = get_metadata(
        notebook,
        "required_files",
        file_list,
    )

    pypi_deps = get_metadata(
        notebook,
        "pypi_dependencies",
        list(config.cookbook_default_pypi_deps),
    )

    if file_deps:
        wgets = [
            "# We also need to get a few files that the cookbook depends on",
            *(
                f"!wget -q '{config.cookbook_required_files_base_uri}/{dep}'"
                for dep in file_deps
            ),
        ]
    else:
        wgets = []

    notebook = insert_cell(
        notebook,
        cell_type="code",
        source=[
            "# Execute this cell to install OpenMM in the Colab environment",
            f"!pip install -q {' '.join(pypi_deps)}",
            *wgets,
        ],
    )

    outpath = outpath.absolute()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open("w") as file:
        json.dump(notebook, file)


def inject_tags_index(notebook: dict) -> dict:
    """Inject an `index` directive containing the notebook's metadata tags"""

    tags = get_metadata(notebook, "tags", ["untagged"])

    return insert_cell(
        notebook,
        cell_type="raw",
        metadata={"raw_mimetype": "text/restructuredtext"},
        source=[
            f".. index:: {', '.join(tags)}",
        ],
    )


def process_notebook(app: Application, docname: str, source: list[str]):
    build_colab = Path(app.outdir) / "colab"

    docpath = Path(app.env.doc2path(docname, False))

    if docpath.suffix == ".ipynb":
        notebook = json.loads(source[0])
        create_colab_notebook(notebook, docpath, build_colab / docpath, app.config)

        source[0] = json.dumps(inject_tags_index(notebook))


def remove_colab_notebook(app: Application, env: BuildEnvironment, docname: str):
    """Remove generated colab notebooks that are no longer needed"""
    outdir = Path(app.outdir)
    colab_path = outdir / "colab" / docname
    colab_path = colab_path.with_suffix(".ipynb")
    # We check is_relative_to just in case docname is absolute
    if colab_path.exists() and colab_path.is_relative_to(outdir / "colab"):
        colab_path.unlink()


def construct_index(app: Application, pagename: str, templatename: str, context: dict[str, Any], doctree: Optional[document]):
    if pagename != "genindex":
        return

    index_data = {}

    for docname, entries in app.env.domains.index_domain.entries.items():
        for _, tag, _, _, _ in entries:
            index_data.setdefault(tag, set()).add(docname)

    def get_title_url(docname):
        if docname in app.env.titles:
            title = app.env.titles[docname].astext()
        else:
            title = docname.split("/")[-1]
        return title, app.builder.get_relative_uri("genindex", docname)

    context["indexdata"] = [(tag, sorted(get_title_url(docname) for docname in docnames)) for tag, docnames in sorted(index_data.items())]

def setup(app: Application):
    app.add_config_value(
        "cookbook_default_pypi_deps",
        default=[],
        rebuild="env",
    )
    app.add_config_value(
        "cookbook_default_required_files",
        default=None,
        rebuild="env",
    )
    app.add_config_value(
        "cookbook_required_files_base_uri",
        default="",
        rebuild="env",
    )

    app.connect("env-purge-doc", remove_colab_notebook)
    app.connect("source-read", process_notebook)
    app.connect("html-page-context", construct_index)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
