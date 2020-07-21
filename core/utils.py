
def get_object(*args, **kwargs):

    from django.shortcuts import get_object_or_404

    from django.http import Http404
    try:
        get_object_or_404(*args, **kwargs)
    except Http404 as http404:
        from rest_framework.exceptions import APIException
        raise APIException(detail=str(http404), code=404)
