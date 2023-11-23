from django.contrib import admin
from django.urls import path, include #include와 urls를 사용하기위해 import 해줘야 하는것

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')), #elections app을 include 해주는것임.
]


