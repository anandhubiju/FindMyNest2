from django.contrib import admin
from django.urls import path,include
from allauth.account.views import login, logout
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    
    path('',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('propertys/',views.propertys,name='propertys'),
    path('users/',views.users,name='users'),
    path('subscription/',views.subscription,name='subscription'),
    path('accounts/', include('allauth.urls')),
    path('googleProfileComplte/', views.googleProfileComplte, name='googleProfileComplte'),
    path('view_all_users/',views.view_all_users,name='view_all_users'),
    

    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('register/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    
    path('deleteUser/<int:delete_id>',views.deleteUser,name="deleteUser"),
    path('updateStauts/<int:update_id>',views.updateStatus,name="updateStatus"),
    path('user_details/<int:user_id>/', views.user_details, name='user_details'),  
    path('updateuserStauts/<int:update_id>',views.updateuserStatus,name="updateuserStatus"),
    path('property/<int:property_id>/delete/', views.delete_property, name='adelete_property'),
    
    
]