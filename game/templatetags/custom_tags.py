
# es necesario crear un filtro personalizado para añadir clases a los campos de los formularios, ya que no se pueden añadir directamente en el template.
#  es como que django no reconoce las clases de bootstrap en los formularios, por lo que hay que añadirlas manualmente.
from django import template


register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    css_classes += ' ' + arg
    return value.as_widget(attrs={'class': css_classes})

# aplicar bootsttrap a game.html
# {% extends "base.html" %}
# {% load custom_tags %}


