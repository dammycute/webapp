from django.urls import path
from .views import *
urlpatterns = [
    path('post-property/', CreatePropertyView.as_view()),
    path('post-property/<int:id>/', UpdatePropertyView.as_view()),

]