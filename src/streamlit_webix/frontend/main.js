// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

/**
 * The component's render function. This will be called imediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  if (!window.rendered) {
    window.rendered = true
    let args = event.detail.args;
    let config = structuredClone(args.config);
    let height = args.height;

    const script = document.createElement('script');
    script.src = args.js_link;
    script.type = "text/javascript";
    document.head.appendChild(script);

    const link = document.createElement('link');
    link.href = args.css_link;
    link.rel = 'stylesheet';
    document.head.appendChild(link);

    script.addEventListener('load', () => {
      if (args.allow_unsafe_jscode) {
        config = deepMap(config, parseJsCodeFromPython)
      }

      // You most likely want to get the data passed in like this
      // const {input1, input2, input3} = event.detail.args

      webix.ui(
        config
      );
      if(height) {
        Streamlit.setFrameHeight(height);
      } else {
        Streamlit.setFrameHeight(200);
      }
    })
  }
}

// stole from https://github.com/andfanilo/streamlit-echarts/blob/master/streamlit_echarts/frontend/src/utils.js Thanks andfanilo
function mapObject(obj, fn, keysToIgnore) {
    let keysToMap = Object.keys(obj)
    return keysToMap.reduce((res, key) => {
        if (!keysToIgnore.includes(key)) {
            res[key] = fn(obj[key]);
            return res
        }
        res[key] = obj[key];
        return res

    }, {})
}

function deepMap(obj, fn, keysToIgnore = []) {
    const deepMapper = (val) =>
        val !== null && typeof val === "object" ? deepMap(val, fn) : fn(val)
    if (Array.isArray(obj)) {
        return obj.map(deepMapper)
    }
    if (typeof obj === "object") {
        return mapObject(obj, deepMapper, keysToIgnore)
    }
    return obj
}

function parseJsCodeFromPython(v) {
  const JS_PLACEHOLDER = "::JSCODE::"
  let funcReg = new RegExp(
    `${JS_PLACEHOLDER}(.*)${JS_PLACEHOLDER}`
  )

  let match = funcReg.exec(v)

  if (match) {

    const funcStr = match[1]
    // eslint-disable-next-line
    return new Function("return " + funcStr)()
  } else {
    return v
  }
}


// export Streamlit library (so users can call setComponentValue from JsCode)
window.Streamlit = Streamlit;
// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
