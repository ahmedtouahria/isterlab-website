from django.http import JsonResponse


def healthz(request):
    return JsonResponse({'status': 'ok'})


class HealthCheckMiddleware:
    """Allow internal probes even when production redirects HTTP to HTTPS."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/healthz/':
            return healthz(request)
        return self.get_response(request)
