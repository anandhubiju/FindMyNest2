from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [  
    path('',views.addproperty,name='addproperty'),
    path('propertylist/',views.propertylist,name='propertylist'),
    path('property_single/<int:property_id>/',views.propertysingle,name='property_single'),
    path('update_property/<int:property_id>/', views.update_property, name='update_property'),
    path('delete_property/<int:property_id>/', views.delete_property, name='delete_property'),
    path('edit_property/<int:property_id>/', views.edit_property, name='edit_property'),
    path('property_list_by_type/<str:property_type>/', views.property_list_by_type, name='property_list_by_type'),
    path('submit-comment/', views.submit_comment, name='submit_comment'),
    path('like_feedback/<int:feedback_id>/',views.like_feedback, name='like_feedback'),
    path('add_wishlist/<int:property_id>/', views.add_wishlist, name='add_wishlist'),
    path('delete_wishlist/<int:property_id>/', views.delete_wishlist, name='delete_wishlist'),
    path('wishlist_view/',views.wishlist_view,name='wishlist_view'),
    path('viewcontact/<int:property_id>/', views.viewcontact, name='viewcontact'),

    
]