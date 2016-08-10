from django import template

def list_fields(model):
	return [field.name for field in model._meta.get_fields() 
						if not field.is_relation and field.name != 'id' ]

def get_value(model, value):
	return getattr(model, value)

register = template.Library()
register.filter('list_fields', list_fields)
register.filter('get_value', get_value)