from django.urls import path
from .views import ApiView

urlpatterns = [
    path('api/hello', ApiView.as_view(), name='view' ),
]
