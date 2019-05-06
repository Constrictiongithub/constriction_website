from django import template
from django.urls import resolve
from django.urls import reverse
from django.urls import translate_url
from django.utils import translation

register = template.Library()

@register.simple_tag(takes_context=True)
def change_language(context, lang=None, *args, **kwargs):
    path = context['request'].path
    url_parts = resolve(path)
    cur_language = translation.get_language()
    try:
        translation.activate(lang)
        if 'investment' in context:
            slug = context['investment'].slug
            url = reverse(url_parts.view_name, kwargs={'slug': slug})
        else:
            url = reverse(url_parts.view_name, kwargs=url_parts.kwargs)
    finally:
        translation.activate(cur_language)
    return url
