from django.shortcuts import render, get_object_or_404
from core.models.data_objects.blog import Blog

from django.http import JsonResponse, HttpResponse

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, "core/pages/blog_page/blogs_list.html", {"blogs": blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, "core/pages/blog_page/blog_page.html", {"blog": blog})

def chat_page_view(request):
    return render(request, "core/openai_client/openai_client.html")
