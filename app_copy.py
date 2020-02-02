from flask import Flask, render_template, jsonify, request, url_for
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, AjaxDataSource
from bokeh.models import CustomJS, Slider, Select
from bokeh.layouts import widgetbox, column
import json
import math

# Some parts of the code was addopted from https://stackoverflow.com/questions/37083998/flask-bokeh-ajaxdatasource

resources = INLINE
js_resources = resources.render_js()
css_resources = resources.render_css()

app = Flask(__name__)

# To prevent caching files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
    x = [x*0.005 for x in range(0, 200)]
    y = x
    source = ColumnDataSource(data=dict(x=x, y=y))

    plot = figure(plot_width=300, plot_height=250)
    plot.line('x', 'y',  line_width=3, source=source, line_alpha=0.6)

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var f = cb_obj.value
        x = data['x']
        y = data['y']
        for (i = 0; i < x.length; i++) {
            y[i] = Math.pow(x[i], f)
        }
        source.trigger('change');
    """)

    slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
    slider.js_on_change('value', callback)

    layout = column(slider, plot)
    script, div = components(layout, INLINE)
    return render_template('bokeh.html',
                           script=script,
                           div=div,
                           js_resources=INLINE.render_js(),
                           css_resources=INLINE.render_css())


my_data = {'one': [1, 3, 5],
           'two': [2, 7, 5],
           'three': [8, 3, 6]}


if __name__ == "__main__":
    app.run(debug=True)
