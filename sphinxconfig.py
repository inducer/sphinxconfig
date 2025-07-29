from os.path import basename as _basename, dirname as _dirname


html_theme = "furo"
html_show_sourcelink = True

project = _basename(_dirname(_dirname(__file__)))

autoclass_content = "class"

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True


def linkcode_resolve(
        domain: str,
        info: dict[str, str],
        linkcode_url: str | None = None,
        ) -> str | None:
    import inspect
    import os
    import sys

    if domain != "py" or not info["module"]:
        return None

    submodname = info["module"]
    topmodname = submodname.split(".")[0]
    fullname = info["fullname"]

    topmod = sys.modules.get(topmodname)
    submod = sys.modules.get(submodname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    try:
        modpath = os.path.dirname(os.path.dirname(inspect.getsourcefile(topmod)))
        filepath = os.path.relpath(inspect.getsourcefile(obj), modpath)
    except Exception:
        return None

    if filepath is None:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except OSError:
        return None
    else:
        linestart, linestop = lineno, lineno + len(source) - 1

    if linkcode_url is None:
        linkcode_url = (
            f"https://github.com/inducer/{project}/blob/"
            + "main"
            + "/{filepath}#L{linestart}-L{linestop}"  # noqa: RUF027
        )

    return linkcode_url.format(
        filepath=filepath, linestart=linestart, linestop=linestop
    )


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.doctest",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
]

__all__ = (
    "autoclass_content",
    "copybutton_prompt_is_regexp",
    "copybutton_prompt_text",
    "extensions",
    "html_show_sourcelink",
    "html_theme",
    "linkcode_resolve",
    "project",
)
