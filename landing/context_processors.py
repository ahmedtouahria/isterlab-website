from .models import Service,Solution


def global_context(request):

    global_services = Service.objects.all()[:6]
    global_solutions = Solution.objects.all()[:6]
    context = {
        "constance_services": global_services,
        "constance_solutions": global_solutions
    }

    return context