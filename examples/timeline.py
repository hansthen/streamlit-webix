import streamlit as st
from streamlit_webix import ui, JsCode
st.set_page_config(layout="wide")

time_data = [
    {"id": 1, "value": "Available", "date": "2017-08-01"},
    {"id": 2, "value": "Taken", "details": "by Malcolm Merlyn", "date": "2017-09-10"},
    {"id": 3, "value": "Broken", "date": "2017-12-11"},
    {"id": 5, "value": "Fixed", "date": "2018-02-10"},
    {"id": 6, "value": "Available", "date": "2018-03-15"},
    {"id": 7, "value": "Taken", "details": "by Rosa White", "date": "2018-03-21"},
    {"id": 8, "value": "Broken", "date": "2019-05-16"},
    {"id": 9, "value": "Fixed", "date": "2019-06-02"},
    {"id": 10, "value": "Available", "date": "2019-09-10"},
    {"id": 11, "value": "Deprecated", "date": "2019-09-23"},
]
config = {
    "view": "timeline",
    "type": {
        "type": "left",
        "lineColor": "orange",
        "templateDate": JsCode("(obj) => webix.i18n.longDateFormatStr(obj.date)"),
    },
    "id": "timeline1",
    "width": 1400,
    "data": time_data
}
ui(config, height=800, allow_unsafe_jscode=True)
