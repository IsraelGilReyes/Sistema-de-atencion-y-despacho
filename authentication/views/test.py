from django.shortcuts import render

def api_test(request):
    """
    Vista para mostrar la página de prueba de la API
    """
    return render(request, 'api_test.html') 