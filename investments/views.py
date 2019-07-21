from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_countries import countries as available_countries
from investments.models import CATEGORY_CHOICES
from investments.models import SOURCE_CHOICES
from investments.models import Investment


class UnderConstruction(TemplateView):
    template_name = "under-construction.html"


class HomePage(ListView):
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


class InvestmentList(ListView):
    paginate_by = 9
    context_object_name = "investments"
    ordering = ['-created']


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
            investments = investments.filter(country__in=self.countries)
        return investments.prefetch_related('images')

    def _get_filter(self, key, CHOICES):
        selected = self.request.GET.getlist(key, [])
        for item in CHOICES:
            value, name = item
            is_selected = False
            if value in selected:
                is_selected = True
            yield {"title": name, "value": value, "selected": is_selected}

    def get_country_filter(self):
        return self._get_filter("country", list(available_countries))

    def get_category_filter(self):
        return self._get_filter("category", CATEGORY_CHOICES)


class InvestmentDetail(DetailView):
    model = Investment
    context_object_name = "investment"

    def graph_qs(self):
        qs_list = [("country", country.code) for country in self.object.country]
        qs_list.append(("country", "EU"))
        return urlencode(qs_list)


class Dashboard(TemplateView):
    pass
