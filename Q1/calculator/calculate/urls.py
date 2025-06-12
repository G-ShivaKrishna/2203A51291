
from django.urls import path
from .views import number_handler_view
urlpatterns=[
    path('numbers/<str:identifier>/',number_handler_view),
]
