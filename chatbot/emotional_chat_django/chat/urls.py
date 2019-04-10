from django.urls import path
from . import views

app_name = 'Chat'

urlpatterns = [
	path('reply',views.reply,name="reply"),
	path('suggestsong',views.suggestsong,name="suggestsong"),
	path('',views.index,name="index"),
]
