from django.shortcuts import render


def index(request):
    visits = int(request.COOKIES.get('visits', 0))
    visits += 1
    response = render(request, 'main/index.html', {'visits': visits})
    response.set_cookie('visits', visits)

    return response
