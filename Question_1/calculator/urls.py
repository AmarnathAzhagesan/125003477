from django.urls import path
from .views import NumberView

urlpatterns = [
    path('<str:number_id>/', NumberView.as_view(), name='number_view'),
]
