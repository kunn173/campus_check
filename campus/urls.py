from django.urls import path
from campus import views


app_name = 'universities'


urlpatterns = [

    path('', views.university_list, name='university_list'),
    path('university_detail/<int:pk>/', views.university_detail, name='university_detail'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('courses/<int:course_id>/submit_review/', views.submit_review, name='submit_review')


]

