from django.http import HttpResponse

def home_view(request):
    """Простое представление, возвращающее текст при переходе на главную страницу."""
    return HttpResponse("Привет! Это главная страница сайта на Django.")
