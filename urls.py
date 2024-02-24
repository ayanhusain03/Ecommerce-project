"""
URL configuration for ecomm project.

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
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path("signout/",views.signout,name="signout"),
    path('product_details/<int:pid>',views.product_details,name="product_details"),
    path('addCart/<int:pid>',views.addCart,name="addCart"),
    path('viewCart',views.viewCart,name="viewCart"),
    path('updateqty/<int:val>/<int:pid>',views.updateqty,name="updateqty"),
    path('remove_product/<int:pid>',views.remove_product,name="remove_product"),
    path('search_product/',views.search_product,name="search_product"),
    path('subcategories/<str:name>',views.subcategories,name=""),
    path('viewOrder/',views.viewOrder,name="viewOrder"),
    path('payment/',views.payment,name="payment")

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)