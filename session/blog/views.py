from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Blog, Comment, Tag,Like


def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)
    tags = blog.tag.all()
    likes = len(Like.objects.filter(blog=blog))  #해당 블로그의 모든 좋아요 가져오기

    return render(request, 'detail.html', {'blog': blog, 'comments': comments, 'tags': tags, 'likes':likes})


def new(request):
    tags = Tag.objects.all()
    return render(request, 'new.html', {'tags': tags})


def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.author = request.user

    new_blog.save()
    tags = request.POST.getlist('tags')

    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        new_blog.tag.add(tag)

    return redirect('detail', new_blog.id)


def edit(request, blog_id):
    # edit_blog = get_object_or_404(Blog, pk=blog_id)
    edit_blog = Blog.objects.get(id=blog_id)

    if request.user != edit_blog.author:
        return redirect('home')

    return render(request, 'edit.html', {'edit_blog': edit_blog})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)


def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    if request.user == delete_blog.author:
        delete_blog.delete()
        return redirect('home')
    return redirect('detail', delete_blog.id)   


def create_comment(request, blog_id):
    comment = Comment()
    comment.content = request.POST.get('content')
    comment.blog = get_object_or_404(Blog, pk=blog_id)
    comment.author = request.user
    comment.save()
    return redirect('detail', blog_id)


def new_comment(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'new_comment.html', {'blog': blog})


def like(request, blog_id):
    #로그인하지 않았다면 -> 좋아요 못 누르고, 로그인 페이지로 이동
    if request.user.is_anonymous:
        return redirect("users:signin")
    
    #현재 로그인 사용자가 해당 글에 Like 객체 만든 것이 존재한다면 -> detail path로 이동
    if Like.objects.filter(likedUser = request.user, blog_id=blog_id): #이미 좋아요 누름
        return redirect("detail", blog_id)
    
    # 현재 로그인 사용자가 해당 글에 Like 객체 만든 것이 존재하지 않는다면 -> Like 객체 만들기
    like = Like() #라이크 객체 생성
    like.blog = get_object_or_404(Blog, pk = blog_id) 
    like.likedUser = request.user
    like.save()
    return redirect("detail", blog_id)   
        