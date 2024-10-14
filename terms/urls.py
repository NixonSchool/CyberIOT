from django.urls import path
from . import views

app_name = 'terms'

urlpatterns = [
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('data-collection-info/', views.data_collection_info, name='data_collection_info'),
    path('user-data-download/', views.user_data_download, name='user_data_download'),
    path('download-data/', views.download_data, name='download_data'),
    path('about/', views.about, name='about'),
]
