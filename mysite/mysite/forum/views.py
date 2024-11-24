from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from .forms import CommentForm, AccountForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

User = get_user_model()


def index(request):
    comments = Comment.objects.all()
    return render(request, 'forum/index.html', {'comments': comments})


def log_in(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Отримані дані: username={username}, password={password}")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = redirect('forum:profile')

            response.set_cookie('username', username)
            response.set_cookie('login_status', True)
            print("Успішна автентифікація")
            print(response.cookies)
            return response
        else:
            messages.error(request, 'Неправильний логін або пароль.')
            print("Помилкові дані")
            return redirect('forum:login')

    else:
        form = AccountForm()

    return render(request, 'forum/login.html', {'form': form})


def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum:login')
        else:
            print(form.errors)
    else:
        form = AccountForm()

    return render(request, 'forum/create_account.html', {'form': form})


def create_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            if len(comment.text) < 2:
                form.add_error('text', 'Comment must be at least 2 characters long')
            else:
                comment.save()
                return redirect('forum:home')
    else:
        form = CommentForm()
    return render(request, 'forum/create_comment.html', {'form': form})


def change_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('forum:profile')
    else:
        form = CommentForm(instance=comment)

    return render(request, 'forum/change_comment.html', {'form': form, 'comment': comment})


def profile(request):
    if not request.user.is_authenticated:
        return redirect('forum:login')

    user_comments = Comment.objects.filter(user=request.user)
    return render(request, 'forum/profile.html', {'comments': user_comments})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'POST':
        comment.delete()
        return redirect('forum:profile')

    form = CommentForm(instance=comment)
    form.fields['text'].widget.attrs['disabled'] = True

    return render(request, 'forum/delete_comment.html', {'form': form, 'comment': comment})
