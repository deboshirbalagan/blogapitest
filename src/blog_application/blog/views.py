from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.http import Http404

def index(request):


    posts_list = Post.objects.all()

    search = request.GET.get('q')

    if search:
        posts_list = posts_list.filter(Q(text__icontains=search))

    context={
        'posts_list' : posts_list,
    }

    return render(request, 'blog/index.html', context)

def detail(request, id=None):
    try:

        post = get_object_or_404(Post, id=id)

    except Http404:

        return render(request, 'blog/404.html', {})

    context = {
        'post': post
    }

    return render(request, 'blog/detail.html', context)

def create_post(request):
    if request.method =='POST':

        f = PostForm(request.POST)

        if f.is_valid():
            post = f.save()

            return redirect('blog:index')

    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'blog/create_post.html', context)

def edit_post(request, id = None):
    try:

        post = get_object_or_404(Post, id=id)

    except Http404:

        return render(request, 'blog/404.html', {})

    if request.method =='POST':

        f = PostForm(request.POST, instance=post)

        if f.is_valid():
            post = f.save()

            return redirect('blog:index')

    else:

        form = PostForm(instance=post)

    context = {
        'form': form
    }

    return render(request, 'blog/create_post.html', context)

def delete_post(request, id=None):
    try:

        post = get_object_or_404(Post, id=id)

    except Http404:

        return render(request, 'blog/404.html', {})

    post.delete()

    return redirect('blog:index')

def like_post_index(request, id=None):

    post = post = get_object_or_404(Post, id=id)
    post.likes += 1
    post.save()

    return redirect('blog:index')

def like_post(request, id=None):

    post = post = get_object_or_404(Post, id=id)
    post.likes += 1
    post.save()

    return redirect('blog:detail', id)

