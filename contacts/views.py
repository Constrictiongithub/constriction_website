from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from .forms import ContactForm


class ContactsView(View):
    form_class = ContactForm
    template_name = 'contacts.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # send email code goes here
            return HttpResponse('Thanks for contacting us!')
        return self.get(request, args, kwargs)
