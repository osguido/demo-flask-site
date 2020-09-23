import pandas as pd
from threading import Thread
from flask import Flask,render_template,request,redirect
import simplejson as json
import requests
import datetime
import jinja2
from alpha_vantage.timeseries import TimeSeries
from bokeh.embed import server_document, components 
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool, TextInput, CustomJS
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
#from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)
app.vars={}
@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

def get_stock(name_stock):
	ts = TimeSeries(key='6A8O57AUA2PDKNDJ', output_format='pandas')
	data, meta_data = ts.get_weekly(symbol=name_stock)
	df = data	 
	return data

def generate_plot(symbol):
	stock_data = get_stock(symbol)
	stock_data = stock_data.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
	stock_data.reset_index(inplace=True)
	stock_data.index = pd.to_datetime(stock_data.index)
	mask = (stock_data.index >= '2020-01-01')
	stock_data = stock_data.loc[mask]
	stock_data1 = stock_data[[ 'Open', 'Close']]
	plot_stock = figure(plot_width=800 ,plot_height=800, x_axis_type="datetime")
	plot_stock.title.text = 'Monthly Stock Data of %s' % app.vars['symbol'].upper()
	plot_stock.xaxis.axis_label = "Date and Month of 2020"
	plot_stock.yaxis.axis_label = "Price"
	plot_stock.axis.axis_line_color = None
	plot_stock.title.text_font_size = "18px"
	plot_stock.line(stock_data1.index, stock_data1['Open'], line_width=2, line_color='blue', name='Open')
	script, div = components(plot_stock)
	return script, div; 

@app.route("/plot",methods=['POST'])
def plot():
    symbol = app.vars['symbol'] = request.form['symbol']
    script_d, div_d = generate_plot(symbol)
    return render_template("plot.html" , script = script_d, div=div_d)




if __name__ == '__main__':
   app.run(port=33507)
