from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_countries import countries as available_countries
from investments.models import CATEGORY_CHOICES
from investments.models import Investment


class UnderConstructionView(TemplateView):
    template_name = "under-construction.html"


class HomePageView(ListView):
    template_name = "home.html"
    model = Investment
    paginate_by = 6
    context_object_name = "investments"
    ordering = ['-created']

    def get_queryset(self):
        investments = Investment.objects.all()
        return investments.prefetch_related('images')

    def count_realestate(self):
        return Investment.objects.filter(category="immobili").count()

    def count_financial(self):
        return Investment.objects.filter(category="finanza").count()
    
    def count_countries(self):
        return len(Investment.objects.order_by("country").values('country').distinct())

    def count_users(self):
        return 5

class InvestmentsView(ListView):
    paginate_by = 9
    context_object_name = "investments"
    ordering = ['-created']

    def get_queryset(self):
        investments = Investment.objects.all()
        price = self.get_price()
        categories = self.request.GET.getlist("category", [])
        countries = self.request.GET.getlist("country", [])
        if price:
            investments = investments.filter(price__range=(int(p) for p in price.split(";")))
        if categories:
            investments = investments.filter(category__in=categories)
        if countries:
            investments = investments.filter(country__in=countries)
        return investments.prefetch_related('images')

    def get_price(self):
        price = self.request.GET.get("price")
        if price:
            return price
        return "0;50000000"

    def get_filter(self, key, CHOICES):
        selected = self.request.GET.getlist(key, [])
        for item in CHOICES:
            value, name = item
            is_selected = False
            if not selected or value in selected:
                is_selected = True
            yield {"title": name, "value": value, "selected": is_selected}

    def get_country_filter(self):
        return self.get_filter("country", list(available_countries))

    def get_category_filter(self):
        return self.get_filter("category", CATEGORY_CHOICES)


class InvestmentView(DetailView):
    model = Investment
    context_object_name = "investment"

    def graph_qs(self):
        return urlencode([("country", self.object.country.code), ("country", "EU")])
