from flask import Flask, render_template
import urllib.request, json 
from pandas.io.json import json_normalize 

app = Flask(__name__)

@app.route('/')
def index():
	with urllib.request.urlopen("https://api.covid19india.org/data.json") as url:
		raw_data = json.loads(url.read().decode())
	df = json_normalize(raw_data['statewise']) 
	df_state = df.set_index('state')

	totalEARD = {"Effected":df_state.loc['Total']['confirmed'],'Active':df_state.loc['Total']['active'],'Recovered':df_state.loc['Total']['recovered'],'Decreased':df_state.loc['Total']['deaths']}
	deltaERD = {'Effected':df_state.loc['Total']['deltaconfirmed'],'Recovered':df_state.loc['Total']['deltarecovered'],'Decreased':df_state.loc['Total']['deltadeaths']}
	
	return render_template('index.html',totalEARD=totalEARD,deltaERD=deltaERD,TodayDateTime=df_state.loc['Total']['lastupdatedtime'])