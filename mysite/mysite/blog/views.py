from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .models import BlogPost, CommentForBlogPost
from django.urls import reverse_lazy
from .forms import CommentForBlogPostForm, EmailForm
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.core.mail import send_mail


class BlogListView(ListView):
    paginate_by = 5
    model = BlogPost
    template_name = 'blog/blogpost_list.html'

    def get_queryset(self):
        sort_order = self.request.GET.get('sort', '-created_at')
        tag = self.request.GET.get('tag', None)
        queryset = BlogPost.published_objects.all()
        if tag:
            queryset = queryset.filter(tags__name__icontains=tag)

        return queryset.order_by(sort_order)


@method_decorator(login_required(login_url='/blog/login/'), name='dispatch')
class UserBlogListView(ListView, LoginRequiredMixin):
    paginate_by = 5
    model = BlogPost
    template_name = 'blog/user_blogpost_list.html'
    context_object_name = 'blogposts'
    login_url = '/blog/login/'

    def get_queryset(self):
        sort_order = self.request.GET.get('sort', '-created_at')
        tag = self.request.GET.get('tag', None)
        queryset = BlogPost.objects.filter(owner=self.request.user)
        if tag:
            queryset = queryset.filter(tags__name__icontains=tag)

        return queryset.order_by(sort_order)


class BlogDetailView(DetailView):
    model = BlogPost
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = CommentForBlogPost.objects.filter(post=self.get_object()).order_by('-created_at')
        paginator = Paginator(comments, 7)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['form'] = CommentForBlogPostForm()
        context['email_form'] = EmailForm()
        return context

    def post(self, request, *args, **kwargs):
        blog_post = self.get_object()
        form = CommentForBlogPostForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog_post
            comment.owner = request.user
            comment.save()

            return redirect('blog:post', slug=blog_post.slug)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class BlogUpdateView(UpdateView):
    model = BlogPost
    success_url = reverse_lazy('blog:posts')
    fields = ['title', 'text', 'tags']

    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner = self.request.user)
        return qset

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(BlogPost, slug=slug)


class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:posts')

    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner = self.request.user)
        return qset

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(BlogPost, slug=slug)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'text', 'tags']
    success_url = '/blog/posts/'
    login_url = '/blog/login/'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        form.save_m2m()
        return super(BlogCreateView, self).form_valid(form)


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'blog/register.html'
    success_url = '/blog/posts/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        print("User logged in:", self.request.user.is_authenticated)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'blog/login.html'
    success_url = '/blog/posts/'


class CommentUpdateView(UpdateView):
    model = CommentForBlogPost
    success_url = reverse_lazy('blog:post', kwargs={'slug': 'slug_placeholder'})
    fields = ['text']

    def get_queryset(self):
        qset = super().get_queryset()
        qset = qset.filter(owner=self.request.user)
        return qset

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        comment_slug = self.kwargs.get('comment_slug')
        return get_object_or_404(CommentForBlogPost, slug=comment_slug, blog_post__slug=slug, owner=self.request.user)


class CommentDeleteView(DeleteView):
    model = CommentForBlogPost
    success_url = reverse_lazy('blog:post', kwargs={'slug': 'slug_placeholder'})

    def get_queryset(self):
        qset = super().get_queryset()
        qset = qset.filter(owner=self.request.user)
        return qset

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        comment_slug = self.kwargs.get('comment_slug')
        return get_object_or_404(CommentForBlogPost, slug=comment_slug, blog_post__slug=slug, owner=self.request.user)


@require_POST
def share_post(request, slug, **kwargs):
    post_obj = get_object_or_404(BlogPost, slug=slug)
    post_abs_url = reverse('blog:post', kwargs={'slug': slug})
    print('dsa')
    form = EmailForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        data.text += f'Post url: {post_abs_url}'
        send_mail(
            data.subject,
            data.text,
            "from@example.com",
            [data.to],
            fail_silently=False,
        )
        print(f'@@@ Sending email to {data}')

    return redirect(post_abs_url)