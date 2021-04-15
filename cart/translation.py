from modeltranslation.translator import TranslationOptions,register
from .models import State,City


@register(City)
class CityTransOptions(TranslationOptions):
    fields = ['name']

@register(State)
class StateTransOptions(TranslationOptions): 
    fields = ['name']