from django.shortcuts import render, get_object_or_404
from .models.blog import Blog

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, "core/blog_page/blogs_list.html", {"blogs": blogs})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, "core/blog_page/blog_page.html", {"blog": blog})
