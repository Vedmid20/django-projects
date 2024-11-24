from jinja2 import Environment
from django.template import engines


def environment(**options):
    env = Environment(**options)

    return env
