from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag, Comment
from Nation.models import Nation
from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.http import Http404


class Home(ListView):
    model = Post
    template_name = 'news/home.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.order_by('-created_at')


class PostsByCategory(ListView):
    template_name = 'news/category.html'
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = False

    def get_queryset(self):
        queryset = Post.objects.filter(category__slug=self.kwargs['slug']).order_by('-created_at')
        if not queryset.exists():
            raise Http404("No posts found in this category.")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

class PostsByNation(ListView):
    template_name = 'news/nation.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        queryset = Post.objects.filter(nation__slug=self.kwargs['slug']).order_by('-created_at')
        if not queryset.exists():
            raise Http404("No posts found from this nation.")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Nation.objects.get(slug=self.kwargs['slug'])
        return context

class GetPost(DetailView):
    model = Post
    template_name = 'news/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        if self.request.user.id not in self.object.seen_by.all():
            self.object.seen_by.add(self.request.user)
        self.object.save()
        self.object.refresh_from_db()

        comments = Comment.objects.filter(post=self.object, is_published=True).order_by('-created_at')
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['comments'] = page_obj
        return context


class PostsByTag(ListView):
    template_name = 'news/tag.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        queryset = Post.objects.filter(tags__slug=self.kwargs['slug']).order_by('-created_at')
        if not queryset.exists():
            raise Http404("No posts found with this tag.")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class Search(ListView):
    template_name = 'news/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post, is_published=True).order_by('-created_at')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        comment_text = request.POST.get('comment')

        name_valid = len(username) >= 2 and all(c.isalnum() or c.isspace() or c in '- ' for c in username)

        try:
            validate_email(email)
            email_valid = True
        except ValidationError:
            email_valid = False

        comment_valid = len(comment_text) >= 2 and all(c.isalnum() or c in ',.-_!? ' for c in comment_text)

        if not (name_valid and email_valid and comment_valid):
            errors = {
                'username': 'Invalid input' if not name_valid else '',
                'email': 'Invalid input' if not email_valid else '',
                'comment': 'Invalid input' if not comment_valid else '',
            }

            context = {
                'post': post,
                'comments': comments,
                'errors': errors,
            }
            return render(request, 'news/single.html', context)

        post = Post.objects.get(pk=post_id)
        comment = Comment(author=request.user, comment=comment_text, post=post)
        comment.save()

        response_data = {
            'success': True,
            'username': comment.username,
            'created_at': comment.created_at.strftime('%d %B %Y'),
            'comment': comment.comment,
        }
        return JsonResponse(response_data)

    context = {
        'post': post,
        'comments': comments,
    }

    return render(request, 'news/single.html', context)