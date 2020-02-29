from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='images',blank=True, null=True)
  title = models.CharField(max_length=200)
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  published_date = models.DateTimeField(blank=True, null=True)

  def publish(self):
    self.published_date = timezone.now()
    self.save()

  def approved_comments(self):
    return self.comments.filter(approved_comment=True)

  def get_absolute_url(self):
    return reverse("post_detail", kwargs={'pk':self.pk})

  def __str__(self):
    return self.title


class Comment(models.Model):
  post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
  author = models.CharField(max_length=200)
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  approved_comment = models.BooleanField(default=False)

  def approve(self):
    self.approved_comment = True
    self.save()
  
  def get_absolute_url(self):
    return reverse("post_list")

  def __str__(self):
    return self.text
