from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
import requests
import  watson_developer_cloud
import json
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
import pandas
import pickle
import urllib.request
import urllib.parse
import re
import random
#0 = sad/dark purple, 1= angry/red, 2 = happy/blue, 3 = neutral/green, 
int_mapper={"anger":1,"sadness":0,"joy":2,"neutral":3}
st=[]
tone_analyzer=watson_developer_cloud.ToneAnalyzerV3(iam_apikey="KlUBlnPrBXFFac0juk4UV8DRcxgFInxcs3isC95rZMdK",url="https://gateway-syd.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21&sentences=False",version="2017-09-21")
mapper={"anger":"anger","fear":"sadness","joy":"joy","sadness":"sadness","analytical":"neutral","confident":"neutral","tentative":"neutral"}
with open("song_popularity.txt", "rb") as fp:   # Unpickling
    l = pickle.load(fp)
with open("ismodel.pkl", "rb") as fp:   # Unpickling
    is_model = pickle.load(fp)

@csrf_exempt
def suggestsong(request):
	req=json.loads(request.body.decode('utf-8') )
	song=req["song"]
	names=is_model.get_similar_items([song])[:5]['song'].tolist()
	print(len(names),names)
	links=[]
	for i in names:
		print(i)
		query_string = urllib.parse.urlencode({"search_query" : i})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		print("http://www.youtube.com/watch?v=" + search_results[0])
		links.append(search_results[0])	
	data={"names":names,"urllink":links}
	return HttpResponse(json.dumps(data),content_type='application/json')

@csrf_exempt
def reply(request):
	req = json.loads(request.body.decode('utf-8') )
	user=req["user"]
	# ----------------------------------------
	text=user.replace("\n"," ")
	tone_analysis=tone_analyzer.tone({'text':text},'application/json').get_result()
	tone=tone_analysis["document_tone"]["tones"]
	tone.sort(key=lambda x: x["score"],reverse=True)
	print("You:"+user)
	print("Tone Analysis:-",tone)
	emotion="neutral"
	if(len(tone)>0):
		emotion=mapper[tone[0]["tone_id"]]
	# ----------------------------------------- 
	global st
	st.append(user)
	if(len(st)>3):
		st=st[-3:]
	print(st)
	print(emotion)
	x=requests.post("http://127.0.0.1:8080/cakechat_api/v1/actions/get_response",
		json={'context':st,'emotion':emotion})
	y=x.json()["response"]
	st.append(y)
	print("Bot:"+y)
	popularity_based_songs=l[int_mapper[emotion]][:20]
	# print(len(popularity_based_songs))
	test=random.sample(range(0, len(popularity_based_songs)), 5)
	test.sort()
	# print(test)
	test2=[]
	for i in test:
		test2.append(popularity_based_songs[i])
	print(test2)
	popularity_based_songs=test2
	# print(len(popularity_based_songs))
	links=[]
	names=[]
	for i in popularity_based_songs:
		print(i['song'])
		names.append(i['song'])
		query_string = urllib.parse.urlencode({"search_query" : i['song']})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		print("http://www.youtube.com/watch?v=" + search_results[0])
		links.append(search_results[0])
	payload={"emotion":emotion,"message":y,"urllink":links,"names":names}
	
	return HttpResponse(json.dumps(payload),content_type='application/json')
    
def index(request):
	global st
	context={}
	# if(request.method=="POST"):
	# 	user=request.POST["sentence"]
	# 	# ----------------------------------------
	# 	text=user.replace("\n"," ")
	# 	tone_analysis=tone_analyzer.tone({'text':text},'application/json').get_result()
	# 	tone=tone_analysis["document_tone"]["tones"]
	# 	tone.sort(key=lambda x: x["score"],reverse=True)
	# 	print("You:"+user)
	# 	print("Tone Analysis:-",tone)
	# 	emotion="neutral"
	# 	if(len(tone)>0):
	# 		emotion=mapper[tone[0]["tone_id"]]
	# 	# ----------------------------------------- 
	# 	st.append(user)
	# 	if(len(st)>3):
	# 		st=st[-3:]
	# 	print(st)
	# 	print(emotion)
	# 	x=requests.post("http://127.0.0.1:8080/cakechat_api/v1/actions/get_response",
	# 		json={'context':st,'emotion':emotion})
	# 	y=x.json()["response"]
	# 	st.append(y)
	# 	print("Bot:"+y)
	return render(request,"index.html",context)
