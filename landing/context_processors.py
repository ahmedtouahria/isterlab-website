from .models import Service,Solution


def global_context(request):

    global_services = Service.objects.all()[:5]
    global_solutions = Solution.objects.all()[:5]
    context = {
        "constance_services": global_services,
        "constance_solutions": global_solutions
    }

    return context