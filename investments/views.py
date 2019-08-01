from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_countries import countries as available_countries

from investments.models import CATEGORY_CHOICES, Investment, RealEstate, P2PLending


class UnderConstruction(TemplateView):
    template_name = "under-construction.html"


class FiltersMixin(object):

    def get_price(self):
        price = self.request.GET.get("price")
        if price:
            return price
        return "0;50000000"

    def get_filter(self, key, choises):
        selected = self.request.GET.getlist(key, [])
        for choise in choises:
            key, title = choise
            is_selected = False
            if not selected or key in selected:
                is_selected = True
            yield {"title": title, "key": key, "selected": is_selected}

    def get_country_filter(self):
        return self.get_filter("country", list(available_countries))

    def get_category_filter(self):
        return self.get_filter("category", CATEGORY_CHOICES)


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
        return investments.prefetch_related('images').select_subclasses()

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
        countries = [c.code for c in self.object.countries] 
        countries.append("EU")
        return urlencode([("country", c) for c in countries])

class RealEstateView(InvestmentView):
    model = RealEstate    


class P2PLendingView(InvestmentView):
    model = P2PLending


class Dashboard(TemplateView):
    pass
