"""
URL configuration for ETR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from apps.users import views as user_view
from apps.trainings import views as training_view
from apps.test_training import views as test_training_view
from apps.enrolls import views as enrolls_view

urlpatterns = [
    
    ## Authentication
    path('register/', user_view.UserAPIView.as_view(), name='Register Account'),
    path('login/', user_view.LoginUserAPIView.as_view(), name='Login'),
    path('updateuser/<int:id>', user_view.UpdateUserAPIVIew.as_view(), name='Update User'),
    path('requestotp/', user_view.OTPAPIView.as_view(), name = 'Request OTP'),
    path('validateotp/', user_view.VerifyOTPAPIView.as_view(), name = 'Verify OTP'),
    path('updatepassword/', user_view.UpdatePasswordAPIView.as_view(), name = 'Update Password'),
    
    ## Training
    path('training/', training_view.TrainingAPIView.as_view(), name = 'Training Management'),
    path('training/<int:id>', training_view.TrainingAPIView.as_view(), name = 'Training Management'),
    
    ## Section
    path('section/', training_view.SectionAPIView.as_view(), name = 'Section Management'),
    path('section/<int:id>', training_view.SectionAPIView.as_view(), name = 'Section Management'),
    
    ## Topic
    path('topic/', training_view.TopicAPIView.as_view(), name = 'Topic Management'),
    path('topic/<int:id>', training_view.TopicAPIView.as_view(), name = 'Topic Management'),
    
    ## Post Test
    path('posttest/', test_training_view.PostTestAPIView.as_view(), name = 'Post Test Management'),
    path('posttest/<int:id>', test_training_view.PostTestAPIView.as_view(), name = 'Post Test Management'),
    
    ## Post Test
    path('answer/', test_training_view.AnswerAPIView.as_view(), name = 'Answer Management'),
    path('answer/<int:id>', test_training_view.AnswerAPIView.as_view(), name = 'Answer Management'),
    
    ## Enroll
    path('enroll/', enrolls_view.EnrollAPIView.as_view(), name = 'Enroll Management'),
    path('enroll/<int:id>', enrolls_view.EnrollAPIView.as_view(), name = 'Enroll Management')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)