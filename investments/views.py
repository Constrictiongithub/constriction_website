from urllib.parse import urlencode

from django.utils.formats import get_format
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_countries import countries as available_countries

from investments.models import (CATEGORY_CHOICES, Investment, P2PLending,
                                RealEstate)


class FiltersMixin(object):

    @property
    def thousand_separator(self):
        return get_format('THOUSAND_SEPARATOR')

    @property
    def min_price(self):
        price = self.request.GET.get("min_price", None)
        if price:
            return int(price)

    @property
    def max_price(self):
        price = self.request.GET.get("max_price", None)
        if price:
            return int(price)

    @property
    def categories(self):
        return self.request.GET.getlist("category", None)

    @property
    def countries(self):
        return self.request.GET.getlist("country", None)

    def _get_filter(self, choices, selected):
        for item in choices:
            value, title = item
            is_selected = False
            if value in selected:
                is_selected = True
            yield {"title": title, "value": value, "selected": is_selected}

    def get_country_filter(self):
        country_choices = [c for c in available_countries if c.code != "EU"]
        return self._get_filter(country_choices, self.countries)

    def get_category_filter(self):
        return self._get_filter(CATEGORY_CHOICES, self.categories)


class HomePageView(TemplateView, FiltersMixin):
    template_name = "home.html"

    def count_realestate(self):
        return Investment.objects.filter(category="immobili").count()

    def count_financial(self):
        return Investment.objects.filter(category="finanza").count()

    def count_countries(self):
        items = Investment.objects.order_by("countries").values('countries')
        return len(items.distinct())

    def count_users(self):
        return 5


class InvestmentsView(ListView, FiltersMixin):
    paginate_by = 9
    context_object_name = "investments"
    ordering = ['-created']

    def get_queryset(self):
        investments = Investment.objects.all()
        if self.min_price:
            if self.max_price:
                prices = (self.min_price, self.max_price)
                investments = investments.filter(price__range=prices)
            else:
                investments = investments.filter(price__gte=self.min_price)
        elif self.max_price:
            investments = investments.filter(price__lte=self.max_price)
        if self.categories:
            investments = investments.filter(category__in=self.categories)
        if self.countries:
            investments = investments.filter(countries__in=self.countries)
        return investments.prefetch_related('images').select_subclasses()


class InvestmentView(DetailView):
    model = Investment
    context_object_name = "investment"

    def graph_qs(self):
        countries = [c.code for c in self.object.countries]
        countries.append("EU")
        return urlencode([("country", c) for c in countries])


class RealEstateView(InvestmentView):
    model = RealEstate


class P2PLendingView(InvestmentView):
    model = P2PLending


class DashboardView(TemplateView):
    pass


class UnderConstructionView(TemplateView):
    template_name = "under-construction.html"
