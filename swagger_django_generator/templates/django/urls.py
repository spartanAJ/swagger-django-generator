"""
Do not modify this file. It is generated from the Swagger specification.

Routing module.
"""
from django.conf.urls import url
from django.conf import settings
import {{ module }}.views as views

urlpatterns = [
    {# URLs are traverse in reversed sorted order so that longer ones are evaluated first #}
    {% for relative_url, class_name in entries|dictsort(true)|reverse %}
    url(r"^{{ relative_url }}$", views.{{ class_name }}.as_view()),
    {% endfor %}
]

if settings.DEBUG:
    urlpatterns.extend([
        url(r"^spec/$", views.__SWAGGER_SPEC__.as_view()),
    ])
