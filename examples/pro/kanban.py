import streamlit as st
from streamlit_webix import ui, JsCode
st.set_page_config(layout="wide")

config = {
    "view": "kanban",
    "id": "board",
    "cols": [
      { "header": "Backlog",
       "body":{ "view":"kanbanlist", "status":"new", "name":"Backlog"}},
      { "header":"In progress",
       "body":{ "margin":0, "padding":8, "rows":[
         { "view":"kanbanheader", "label":"Development", "type":"sub", "icon":"mdi mdi-code-tags"},
         { "view":"kanbanlist", "status":{ "status": "work", "team": 1 },
         "name":"Development"},
         { "view":"kanbanheader", "label":"Design", "type":"sub", "icon":"mdi mdi-pencil"},
         { "view":"kanbanlist", "status":{ "status": "work", "team": 2 },
         "name":"Design"}
       ]}
      },

      { "header":"Test",
       "body":{ "view":"kanbanlist", "status":"test" }},

      { "header":"Done",
       "body":{ "view":"kanbanlist", "status":"done" }}
    ],
    "data": "team_task_set",
    "editor":True
}

ui(config, height=800, allow_unsafe_jscode=True)
