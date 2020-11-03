from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse, redirect
from django.http import (HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect,
                         HttpResponsePermanentRedirect)
from .models import Author, Tag, Category, Post
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import FeedbackForm
from django.core.mail import mail_admins
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from mysite import helpers
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (CreateView, DetailView, UpdateView, DeleteView, ListView)
from django.db import IntegrityError


# import datetime
# from django.conf import settings
# Create your views here.


def test_redirect(request):
    # return HttpResponsePermanentRedirect(reverse('post_list'))
    # return HttpResponseRedirect(reverse('post_list'))
    # return HttpResponseRedirect("/")
    # return redirect('post_list', permanent=True)
    c = Category.objects.get(name='python')
    return redirect(c)


# view function to display a list of posts
# def post_list(request):
#     posts = Post.objects.order_by("-id").all()
#     posts = helpers.pg_records(request, posts, 5)
#     return render(request, 'blog/post_list.html', {'posts': posts})

# using class based view
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-pub_date']
    paginate_by = 5


# def post_detail(request, pk, post_slug):
# try:
#     post = Post.objects.get(pk=pk)
# except ObjectDoesNotExist:
#     # return HttpResponseNotFound("Page not found.")
#     raise Http404("Post not found")
# return render(request, 'blog/post_detail.html', {'post': post})
# using get_object_or_404() method
# post = get_object_or_404(Post, pk=pk)
# return render(request, 'blog/post_detail.html', {'post': post})

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content','category','tags']

    def form_valid(self,form):
        form.instance.author = Author.objects.get(user = self.request.user)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'category', 'tags']

    def form_valid(self, form):
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        a = Author.objects.get(user=self.request.user)

        if a == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        a = Author.objects.get(user=self.request.user)

        if a == post.author:
            return True
        return False


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'blog/category_form.html'
    fields = ['name','slug']

    def form_valid(self,form):
        form.instance.author = Author.objects.get(user = self.request.user)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR,
                                'You already have registered a Category with this name. ' + \
                                'All of your Category names must be unique.')
            return render(request, template_name=self.template_name, context=self.get_context_data())


# view function to display post by category
def post_by_category(request, category_slug):
        category = Category.objects.get(slug=category_slug)
        post = Post.objects.filter(category__slug=category_slug)
        post = helpers.pg_records(request, post, 5)

        context = {
            'category': category,
            'posts': post
        }

        return render(request, 'blog/post_by_category.html', context)


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = 'blog/tag_form.html'
    fields = ['name','slug']

    def form_valid(self,form):
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR,
                                'You already have registered a Category with this name. ' + \
                                'All of your Category names must be unique.')
            return render(request, template_name=self.template_name, context=self.get_context_data())


# view function to display post by tag
def post_by_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    posts = Post.objects.filter(tags=tag)
    posts = helpers.pg_records(request, posts, 5)

    context = {
        'tag': tag,
        'posts': posts
    }

    return render(request, 'blog/post_by_tag.html', context)

# def post_by_category(request, category_slug):
#         category = Category.objects.get(slug=category_slug)
#         post = Post.objects.filter(category__slug=category_slug)
#         post = helpers.pg_records(request, post, 5)
#
#         context = {
#             'category': category,
#             'posts': post
#         }
#
#         return render(request, 'blog/post_by_category.html', context)


def feedback(request):
    if request.method == 'POST':
        f = FeedbackForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data['name']
            sender = f.cleaned_data['email']
            subject = "You have a new Feedback from {}:{}".format(name, sender)
            message = "Subject: {}\n\nMessage: {}".format(f.cleaned_data['subject'], f.cleaned_data['message'])
            mail_admins(subject, message)
            f.save()
            messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            return redirect('feedback')
    else:
        f = FeedbackForm()
    return render(request, 'blog/feedback.html', {'form': f})


def test_cookie(request):
    if not request.COOKIES.get('color'):
        response = HttpResponse("Cookie Set")
        response.set_cookie('color', 'blue')
        return response
    else:
        return HttpResponse("Your favorite color is {0}".format(request.COOKIES['color']))


def track_user(request):
    response = render(request, 'blog/track_user.html')  # store the response in response variable
    if not request.COOKIES.get('visits'):
        response.set_cookie('visits', '1', 3600 * 24 * 365 * 2)
    else:
        visits = int(request.COOKIES.get('visits', '1')) + 1
        response.set_cookie('visits', str(visits), 3600 * 24 * 365 * 2)
    return response


def stop_tracking(request):
    if request.COOKIES.get('visits'):
        response = HttpResponse("Cookies Cleared")
        response.delete_cookie("visits")
    else:
        response = HttpResponse("We are not tracking you.")
    return response


def test_session(request):
    request.session.set_test_cookie()
    return HttpResponse("Testing session cookie")


def test_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("Cookie test passed")
    else:
        response = HttpResponse("Cookie test failed")
    return response


def save_session_data(request):
    # set new data
    request.session['id'] = 1
    request.session['name'] = 'root'
    request.session['password'] = 'rootpass'
    return HttpResponse("Session Data Saved")


def access_session_data(request):
    response = ""
    if request.session.get('id'):
        response += "Id : {0} <br>".format(request.session.get('id'))
    if request.session.get('name'):
        response += "Name : {0} <br>".format(request.session.get('name'))
    if request.session.get('password'):
        response += "Password : {0} <br>".format(request.session.get('password'))

    if not response:
        return HttpResponse("No session data")
    else:
        return HttpResponse(response)


def delete_session_data(request):
    try:
        del request.session['id']
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass

    return HttpResponse("Session Data cleared")


def lousy_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "root" and password == "pass":
            request.session['logged_in'] = True
            return redirect('lousy_secret')
        else:
            messages.error(request, 'Error wrong username/password')
    return render(request, 'blog/lousy_login.html')


def lousy_secret(request):
    if not request.session.get('logged_in'):
        return redirect('lousy_login')
    return render(request, 'blog/lousy_secret_page.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('admin_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('admin_page')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'blog/login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'blog/logout.html')


def admin_page(request):
    if not request.user.is_authenticated:
        return redirect('blog_login')

    return render(request, 'blog/admin_page.html')


def lousy_logout(request):
    try:
        del request.session['logged_in']
    except KeyError:
        return redirect('lousy_login')
    return render(request, 'blog/lousy_logout.html')
