# -*- coding: utf-8 -*-
import re

from collections import OrderedDict


def camel_case(string, upper_first=False):
    """
    Transforms a string from snake_case to camelCase.

    Example:
        >>> camel_case('my_http_method')
        'myHttpMethod'

    Pass upper_first as True to also uppercase the first letter of the
    given string.

    Example:
        >>> camel_case('my_http_method', upper_first=True)
        'MyHttpMethod'
    """
    if upper_first:
        regex = r'(^[a-z])|_([0-9a-z])'
        group = lambda m: m.group(2) if m.group(2) else m.group(1)

    else:
        regex = r'(?!^)_([0-9a-z])'
        group = lambda m: m.group(1)

    return re.sub(regex, lambda match: group(match).upper(), string)


def camelfy(obj, upper_first=False):
    """
    Transforms a JSON object to be camelCased.

    Example:
        >>> some_dict = {'my_request': {'my_http_method': 'GET'}}
        >>> camelfy(some_dict)
        OrderedDict([('myRequest', OrderedDict([('myHttpMethod', 'GET')]))])

    Pass upper_first as True to also uppercase the first letter of each key of
    the given object.

    Example:
        >>> some_dict = {'my_request': {'my_http_method': 'GET'}}
        >>> camelfy(some_dict, upper_first=True)
        OrderedDict([('MyRequest', OrderedDict([('MyHttpMethod', 'GET')]))])
    """
    kwargs = {'upper_first': upper_first}

    transform = lambda value: (
        camelfy(value, **kwargs) if
        isinstance(value, (dict, list)) else value
    )

    if isinstance(obj, list):
        return [transform(value) for value in obj]

    elif isinstance(obj, dict):
        return OrderedDict([
            (camel_case(key, **kwargs), transform(value)) for
            key, value in obj.iteritems()
        ])


def snake_case(string, transform_grouped=True):
    """
    Transforms a string from camelCase to snake_case.

    Example:
        >>> snake_case('myHTTPMethod')
        'my_http_method'

    Pass transform_grouped as False to do not separate uppercase
    grouped letters.

    Example:
        >>> snake_case('myHTTPMEthod', transform_grouped=False)
        'my_httpmethod'
    """
    # Separate grouped uppercase letters eg. myHTTPMethod => myHTTP_Method
    if transform_grouped:
        string = re.sub(r'(?!^)([A-Z]+)([A-Z][0-9a-z])', r'\1_\2', string)

    return re.sub(r'(?!^)([0-9a-z])([A-Z])', r'\1_\2', string).lower()


def snakefy(obj, transform_grouped=True):
    """
    Transforms a JSON object to be snake_cased.
    Returns an OrderedDict instance to maintain properties order.

    Example:
        >>> some_dict = {'myRequest': {'myHTTPMethod': 'GET'}}
        >>> snakefy(some_dict)
        OrderedDict([('my_request', OrderedDict([('my_http_method', 'GET')]))])

    Pass transform_grouped as False to do not separate uppercase
    grouped letters in each ckey of the given object.

    Example:
        >>> some_dict = {'myRequest': {'myHTTPMethod': 'GET'}}
        >>> snakefy(some_dict, transform_grouped=False)
        OrderedDict([('my_request', OrderedDict([('my_httpmethod', 'GET')]))])
    """
    kwargs = {'transform_grouped': transform_grouped}

    transform = lambda value: (
        snakefy(value, **kwargs) if
        isinstance(value, (dict, list)) else value
    )

    if isinstance(obj, list):
        return [transform(value) for value in obj]

    elif isinstance(obj, dict):
        return OrderedDict([
            (snake_case(key, **kwargs), transform(value)) for
            key, value in obj.iteritems()
        ])
