"""constriction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path
from django.utils.translation import gettext_lazy as _
from investments import views

urlpatterns = [
    path(_('investimenti'), views.InvestmentList.as_view(), name='investments'),
    path(_('investimenti/<slug:slug>'), views.InvestmentDetail.as_view(), name='investment'),
    path(_('home'), views.HomePage.as_view(), name='home'),
    path(_('chi-siamo'), views.AboutUs.as_view(), name='about-us'),
    path(_('dashboard'), views.Dashboard.as_view(), name='dashboard'),
    path('', views.UnderConstruction.as_view(), name='under-construction'),
]
