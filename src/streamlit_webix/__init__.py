from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components
import re
from collections.abc import Mapping

# Tell streamlit that there is a component called streamlit_webix,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_webix", path=str(frontend_dir)
)


# stole from https://github.com/andfanilo/streamlit-echarts/blob/master/streamlit_echarts/frontend/src/utils.js Thanks andfanilo
class JsCode:
    def __init__(self, js_code: str):
        """Wrapper around a js function to be injected on gridOptions.
        code is not checked at all.
        set allow_unsafe_jscode=True on webix.ui call to use it.
        Code is rebuilt on client using new Function Syntax (https://javascript.info/new-function)

        Args:
            js_code (str): javascript function code as str
        """
        match_js_comment_expression = r"\/\*[\s\S]*?\*\/|([^\\:]|^)\/\/.*$"
        js_code = re.sub(
            re.compile(match_js_comment_expression, re.MULTILINE), r"\1", js_code
        )

        match_js_spaces = r"\s+(?=(?:[^\'\"]*[\'\"][^\'\"]*[\'\"])*[^\'\"]*$)"
        one_line_jscode = re.sub(match_js_spaces, " ", js_code, flags=re.MULTILINE)

        js_placeholder = "::JSCODE::"
        one_line_jscode = re.sub(r"\s+|\r\s*|\n+", " ", js_code, flags=re.MULTILINE)

        self.js_code = f"{js_placeholder}{one_line_jscode}{js_placeholder}"


def walk_gridOptions(go, func):
    """Recursively walk grid options applying func at each leaf node

    Args:
        go (dict): gridOptions dictionary
        func (callable): a function to apply at leaf nodes
    """

    if isinstance(go, (Mapping, list)):
        for i, k in enumerate(go):
            if isinstance(go[k], Mapping):
                walk_gridOptions(go[k], func)
            elif isinstance(go[k], list):
                for j in go[k]:
                    walk_gridOptions(j, func)
            else:
                go[k] = func(go[k])


# Create the python function that will be called
def ui(
    config: Optional[dict] = {},
    height: Optional[int] = None,
    unsafe_allow_jscode: bool = False,
):
    """
    Add a descriptive docstring
    """
    if unsafe_allow_jscode:
        walk_gridOptions(config, lambda v: v.js_code if isinstance(v, JsCode) else v)

    component_value = _component_func(config=config, height=height)

    return component_value


def main():
    st.write("## Example")
    data = [
        {
            "id": 1,
            "title": "The Shawshank Redemption",
            "year": 1994,
            "votes": 678790,
            "rating": 9.2,
            "rank": 1,
        },
        {
            "id": 2,
            "title": "The Godfather",
            "year": 1972,
            "votes": 511495,
            "rating": 9.2,
            "rank": 2,
        },
    ]
    grid1 = {
        "view": "datatable",
        "columns": [
            {"id": "rank", "header": "", "css": "rank"},
            {"id": "title", "header": "Film title", "fillspace": True},
            {"id": "year", "header": "Released"},
            {"id": "votes", "header": "Votes"},
        ],
        "autoheight": True,
        "scroll": "auto",
        "data": data,
    }

    config = {
        "view": "scrollview",
        "scroll": "y",
        "body": {
            "rows": [
                {"view": "label", "label": "JSON"},
                grid1,
            ]
        },
    }
    value = ui(config)

    st.write(value)


if __name__ == "__main__":
    main()