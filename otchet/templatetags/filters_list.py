# -*- coding: utf-8 -*-
__author__ = 'tich'

from django import template
# from django.utils.datastructures import SortedDict
from collections import OrderedDict

register = template.Library()


@register.filter(name='sort')
def listsort(value):
    if isinstance(value, dict):
        print('dict')
        new_dict = OrderedDict()
        key_list = sorted(value.keys())
        for key in key_list:
            new_dict[key] = value[key]
        print(new_dict)
        return new_dict
    elif isinstance(value, list):
        print('list')
        print(sorted(value))
        return sorted(value)
    else:
        print('no dict')
        print(value)
        return value
    listsort.is_safe = True


