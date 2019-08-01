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
    path(_('investimenti'), views.InvestmentsView.as_view(), name='investments'),
    path(_('investimenti/immobiliari/<slug:slug>'), views.RealEstateView.as_view(), name='realestate'),
    path(_('investimenti/prestiti-p2p/<slug:slug>'), views.P2PLendingView.as_view(), name='p2plending'),
    path(_('investimenti/<slug:slug>'), views.InvestmentView.as_view(), name='investment'),
    path(_('home'), views.HomePageView.as_view(), name='home'),
    path(_('dashboard'), views.DashboardView.as_view(), name='dashboard'),
    path('', views.UnderConstructionView.as_view(), name='under-construction'),
]
