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
        """Wrapper around a js function to be injected on config.
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


def walk(config, func):
    """Recursively walk grid options applying func at each leaf node

    Args:
        go (dict): gridOptions dictionary
        func (callable): a function to apply at leaf nodes
    """

    if isinstance(config, (Mapping, list)):
        for i, k in enumerate(config):
            if isinstance(config[k], Mapping):
                walk(config[k], func)
            elif isinstance(config[k], list):
                for j in config[k]:
                    walk(j, func)
            else:
                config[k] = func(config[k])

# Create the python function that will be called
def ui(
    config: Optional[dict] = {},
    css_link: Optional[str] = "https://cdn.webix.com/edge/webix.css",
    js_link: Optional[str] = "https://cdn.webix.com/edge/webix.js",
    height: Optional[int] = None,
    allow_unsafe_jscode: bool = False,
):
    """
    Add a descriptive docstring
    """
    if allow_unsafe_jscode:
        walk(config, lambda v: v.js_code if isinstance(v, JsCode) else v)

    component_value = _component_func(
        config=config,
        height=height,
        css_link=css_link,
        js_link=js_link,
        allow_unsafe_jscode=allow_unsafe_jscode
    )

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
    value = ui(config, allow_unsafe_jscode=True)

    st.write(value)


if __name__ == "__main__":
    main()
