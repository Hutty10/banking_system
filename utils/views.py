from django.http import JsonResponse


def error_404(request, exception):
    # import pdb;pdb.set_trace()
    message = "The endpoint is not found"
    response = JsonResponse(
        data={
            "message": message,
            "data": {},
            "status": False,
            "status_code": 404,
        }
    )
    response.status_code = 404
    return response


def error_500(request):
    # import pdb;pdb.set_trace()
    message = "An error occured it from us"
    response = JsonResponse(
        data={
            "message": message,
            "data": {},
            "status": False,
            "status_code": 500,
        }
    )
    response.status_code = 500
    return response
