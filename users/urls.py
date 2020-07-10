from django.urls import path, include

from .views import UserList, UserDetail, MyProfile


urlpatterns = [
    path('', UserList.as_view()),
    path('me/', MyProfile.as_view()),   #не менять последовательность
    path('<username>/', UserDetail.as_view()),   
]
