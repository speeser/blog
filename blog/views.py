from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.template import RequestContext
from .models import Post
from .forms import PostForm

# Create your views here.

@login_required
def post_list(request):
    # posts = Post.objects.all()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render( request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form  = PostForm()
    return render( request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return HttpResponseForbidden()
    else:
        post = Post(author=request.user)

    form = PostForm(request.POST or None, instance=post)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)

    return render_to_response( 'blog/post_edit.html', { 'form': form}, context_instance=RequestContext(request))

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('blog.views.post_list')


    
