"""
Do not modify this file. It is generated from the Swagger specification.
Create fixtures file by running "./manage.py dumpdata core auth -o {{ module }}/fixtures/core.json"


"""
import logging
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase, tag
from django.contrib.sessions.middleware import SessionMiddleware


from . import views

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def add_session_to_request(request):
    """Annotate a request object with a session"""
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()


class {{ module|title }}Test(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        try:
            self.user = User.objects.get(id=1)
        except User.DoesNotExist:
            self.user = AnonymousUser
{% for class_name, verbs in classes | dictsort(true) %}
    {% for verb, info in verbs | dictsort(true) %}

    @tag('{{ verb }}', '{{ info.operation }}')
    {% if verb|lower != 'get' %}
    {% set paths = entries[class_name].split('/') %}
    @moto.mock_{{ paths[-2]}}
    {% endif %}
    def test_{{ info.operation }}(self):
        # Create an instance of a {{ verb|upper }} request.
        vars = dict({% for fa in info.form_data %}{{ fa.name }}={% if fa.name=="lab_name" %}"cfscos2"{% elif fa.default %}"{{ fa.default }}" {% else %}None{% endif %}, {% endfor %}{% for ra in info.required_args %}{{ ra.name }}={% if ra.name=="lab_name" %}"cfscos2"{% elif ra.default %}"{{ ra.default }}" {% else %}None{% endif %}, {% endfor %}{% for oa in info.optional_args %}{{ oa.name }}={% if oa.default %}"{{ oa.default }}"{% else %}None{% endif %}, {% endfor %})
        request = self.factory.{{ verb }}('{{ entries[class_name] }}', vars)
        add_session_to_request(request)
        {% if info.secure %}

        # Checking for anonymous user
        # simulating a non-logged-in request
        request.user = AnonymousUser()

        # Test {{ class_name }}.as_view() as if it were deployed at {{ entries[class_name] }}
        response = views.{{ class_name }}.as_view()(request, {% for ra in info.required_args if ra.in == "path" %}{{ ra.name }}={% if ra.name=="username" %}"ajay"{% elif ra.default %}"{{ ra.default }}" {% else %}None{% endif %}, {% endfor %})
        self.assertEqual(response.status_code, 401)
        {% endif %}

        # simulating a logged in user
        request.user = self.user

        # Test {{ class_name }}.as_view() as if it were deployed at {{ entries[class_name] }}
        response = views.{{ class_name }}.as_view()(request, {% for ra in info.required_args if ra.in == "path" %}{{ ra.name }}={% if ra.name=="username" %}"ajay"{% elif ra.default %}"{{ ra.default }}" {% else %}None{% endif %}, {% endfor %})
        print(response.content)
        self.assertEqual(response.status_code, 200)
    {% endfor %}
{% endfor %}
