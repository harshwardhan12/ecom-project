"""
URL configuration for my_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from home.views import *
from django.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', home, name='home'),
                  path('signup/', signup, name='signup'),
                  path('login/', log, name='login'),
                  path('my_cart/', my_cart, name='my_cart'),
                  # path('cart/', add_to_cart, name='cart')
                  path('search', search, name='search'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', home, name='home'),
#     path('signup/', signup, name='signup'),
#     path('login/', log, name='login'),
#     path('cart/', cart, name='cart')

# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# """
# URL configuration for project1 project.

# The urlpatterns list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path, include
# from home.views import *
# from django.views import * 
# from django.conf import settings
# from django.conf.urls.static import static


# urlpatterns = [
#     # path('admin/', admin.site.urls),
#     path('admin/', admin.site.urls),
#     # path('', home, name='home'),
#     path('signup/', signup, name='signup'),
#     path('login/', log, name='login'),
#     path('', home, name='home'),
#     path('my_cart/', my_cart, name='my_cart')
# ]# += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
