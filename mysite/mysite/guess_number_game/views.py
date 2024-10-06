from django.shortcuts import render, redirect
import random


def index(request):
    if 'a' not in request.session or 'b' not in request.session:
        a = random.randint(0, 50)
        b = random.randint(51, 100)
        request.session['a'] = a
        request.session['b'] = b
    else:
        a = request.session['a']
        b = request.session['b']

    print(f"Загадане число: {request.session.get('random_number')}")
    if 'random_number' not in request.session:
        request.session['random_number'] = random.randint(a, b)

        request.session['attempts'] = 0

    message = ""

    if request.method == 'POST':
        user_guess = int(request.POST.get('guess'))
        random_number = request.session['random_number']
        request.session['attempts'] += 1

        if user_guess < random_number:
            message = "More!"
        elif user_guess > random_number:
            message = "Less!"
        else:
            message = f"Great! You guessed the number {random_number} in {request.session['attempts']} attempts."

            del request.session['random_number']
            del request.session['attempts']
            del request.session['a']
            del request.session['b']

    return render(request, 'guess_number_game/index.html', {'message': message, 'a': a, 'b': b})
