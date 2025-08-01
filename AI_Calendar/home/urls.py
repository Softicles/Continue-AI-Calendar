from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home.index'),
    path('add-event/', views.add_event_to_google, name='add_event_to_google'),
    path('delete-event/', views.delete_event_from_google, name='delete_event_from_google'),
    path('ai-process-query/', views.ai_process_query, name='ai_process_query'),
    path('chat-history/', views.get_chat_history, name='chat_history'),
    path('suggested-events/', views.get_event_suggestions, name='get_event_suggestions'),
    path('poll-llm-status/', views.poll_llm_status, name='poll_llm_status'),
    path("privacy/", views.privacy, name="privacy"),
]
