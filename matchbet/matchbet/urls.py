"""matchbet URL Configuration

The `urlpatterns` list routes URLs to views_classes. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views_classes
    1. Add an import:  from my_app import views_classes
    2. Add a URL to urlpatterns:  path('', views_classes.home, name='home')
Class-based views_classes
    1. Add an import:  from other_app.views_classes import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from betlog.views.views import default_view

urlpatterns = [
    path('', default_view),
    path('betlog/', include('betlog.urls')),
    path('admin/', admin.site.urls),
]
