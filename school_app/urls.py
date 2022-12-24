from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.Signup, name='signup'),
    # path('login/', views.MyLoginView.as_view(), name='login'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('user_/', views.MyUserView.as_view(), name='user_'),
    path('other/', views.MyOtherView.as_view(), name='other'),
    path('teacher/',views.TeacherView.as_view(), name='teacher'),
]