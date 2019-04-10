## Chatbot_Emotion_Song_Recommendation ##
--------------------------------------------------------------------------------------------------------------------
Running the Chatbot Server
In the chatbot folder:-

1. first of you need to all install python3
2. then install the requirement.txt file with the following command
	pip install -r requirements.txt
3. open terminal in this folder and run :-
	python tools/download_model.py(only once)( to download the model)	
	python bin/cakechat_server.py
--------------------------------------------------------------------------------------------------------------------
Running the Django Server
In the emotional_chat_django folder:-

1. To run the django server 
	python manage.py runserver
--------------------------------------------------------------------------------------------------------------------
Running it remotely
1. Download ngrok from https://ngrok.com/
2. To get a url to make your system as the server for your application
	./ngrok http 8000
--------------------------------------------------------------------------------------------------------------------

