import json

from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from django.shortcuts import render
from django.views.generic.list import ListView
from economics_data.models import TimeSerie
from economics_data.models import TimeSerieEntry


class JSONResponseMixin():

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs["content_type"] = "application/json"
        return HttpResponse(json.dumps(context), **response_kwargs)
            


class GraphData(JSONResponseMixin, ListView):
    
    def get_queryset(self):
        entries = TimeSerieEntry.objects.select_related('time_serie').filter(time_serie__slug=self.kwargs['slug'])
        countries = self.request.GET.getlist("country", [])
        if countries:
            entries = entries.filter(time_serie__country__in=countries)
        return entries
    
    def render_to_response(self, context, **response_kwargs):
        time_series = []
        for obj in context["object_list"]:
            value = float(obj.value)
            date = obj.date.isoformat()
            serie = obj.time_serie.country.code
            if not any(ts['serie'] == serie for ts in time_series):
                title = obj.time_serie.title
                time_serie = {"serie": serie, "title": obj.time_serie.country.name, "entries": []}
                time_series.append(time_serie)
            else:
                time_serie = next(item for item in time_series if item["serie"] == serie)
            time_serie["entries"].append({"value": value, "date": date})
        return self.render_to_json_response(time_series)
