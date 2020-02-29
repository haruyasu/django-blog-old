from django.utils import timezone
from blog.models import Post, Comment
from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)


class AboutView(TemplateView):
  template_name = 'page/about.html'


class PostListView(ListView):
  model = Post
  template_name = "blog/post_list.html"
  paginate_by = 3

  def get_queryset(self):
    return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
  model = Post
  template_name = "blog/post_detail.html"


class CreatePostView(LoginRequiredMixin, CreateView):
  login_url = '/login/'
  template_name = "blog/post_form.html"
  redirect_field_name = 'blog/post_detail.html'
  form_class = PostForm
  model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
  login_url = '/login/'
  template_name = "blog/post_form.html"
  redirect_field_name = 'blog/post_detail.html'
  form_class = PostForm
  model = Post


class DraftListView(LoginRequiredMixin, ListView):
  login_url = '/login/'
  template_name = "blog/post_draft_list.html"
  model = Post

  def get_queryset(self):
    return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin, DeleteView):
  model = Post
  template_name = "blog/post_confirm_delete.html"
  success_url = reverse_lazy('post_list')


@login_required
def post_publish(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.publish()
  return redirect('post_detail', pk=pk)

@login_required
def post_comment(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = post
      comment.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = CommentForm()
  return render(request, 'blog/post_comment.html', {'form': form})

@login_required
def comment_approve(request, pk):
  comment = get_object_or_404(Comment, pk=pk)
  comment.approve()
  return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
  comment = get_object_or_404(Comment, pk=pk)
  comment.delete()
  return redirect('post_detail', pk=comment.post.pk)
