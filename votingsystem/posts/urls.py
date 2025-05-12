from django.urls import path
from . import views


urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostRetrieveUpdateDestroyView.as_view(), name='delete_post'),
    path('votes/', views.VoteListCreateView.as_view(), name = 'vote_list'),
    path('votes/<int:pk>/', views.VoteListCreateView.as_view(), name = 'vote_create'),
    path('formdata/', views.FormDataCreateView.as_view(), name = 'formdata_list'), 
    path('formdata/<int:pk>/', views.FormDataRetrieveUpdateDestroyView.as_view(), name = 'formdata_update'), 
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
