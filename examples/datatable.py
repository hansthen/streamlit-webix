import streamlit as st
from streamlit_webix import ui

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
