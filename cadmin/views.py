from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from blog.models import Post, Author, Category, Tag
from blog.forms import PostForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from mysite import helpers
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.views.generic import ListView


# Create your views here.
def post_add(request):
    # If request is POST, create a bound form (form with data)
    if request.method == "POST":
        f = PostForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add post form

        # If form is invalid show form with errors again
        if f.is_valid():
            #  save data
            f.save()
            messages.add_message(request, messages.INFO, 'Post added.')
            return redirect('post_add')

    # if request is GET the show unbound form to the user
    else:
        f = PostForm()
    return render(request, 'cadmin/post_add.html', {'form': f})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        f = PostForm(request.POST, instance=post)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'Post updated.')
            return redirect(reverse('post_update', args=[post.id]))

    # if request is GET the show unbound form to the user, along with data
    else:
        f = PostForm(instance=post)

    return render(request, 'cadmin/post_update.html', {'form': f, 'post': post})


# @login_required
# def home(request):
#     return render(request, 'cadmin/admin_page.html')


# def login(request, **kwargs):
#     if request.user.is_authenticated:
#         return redirect('/cadmin/')
#     else:
#         return render(request,'cadmin/login.html')


# def logout(request):
#     auth.logout(request)
#     return render(request,'cadmin/logout.html')


# user registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # send email verification now
            activation_key = helpers.generate_activation_key(username=request.POST['username'])
            subject = 'The Django Blog Account Activation'
            message = f'''\n
                   please click on the link below to activate your account: \n
                   {request.scheme}://{request.get_host()}/cadmin/activate/account/?key={activation_key}
                   '''
            error = False
            try:

                send_mail(subject, message, settings.SERVER_EMAIL, [request.POST['email']])
                messages.success(request,
                                 f'Account created! Click on the link sent to your email to activate the account')
            except:
                error = True
                messages.success(request, 'Unable to send email. Please try again')

            if not error:
                u = User.objects.create_user(request.POST['username'],
                                             request.POST['email'],
                                             request.POST['password1'],
                                             is_active=0)
                author = Author()
                author.activation_key = activation_key
                author.user = u
                author.save()

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'cadmin/register.html', {'form': form})


def activate_account(request):
    key = request.GET['key']
    if not key:
        raise Http404()

    r = get_object_or_404(Author, activation_key=key, email_validated=False)
    r.user.is_active = True
    r.user.save()
    r.email_validated = True
    r.save()

    return render(request, 'cadmin/activated.html')


class UserPostListView(ListView):
    model = Post
    template_name = 'cadmin/user_post_list.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-pub_date']  # does not get called when we use get_queryset method
    paginate_by = 2

    def get_queryset(self):
        a = Author.objects.get(user=self.request.user)
        return Post.objects.filter(author=a).order_by('-pub_date')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                  request.FILES,
                                  instance=request.user.author)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile Updated!')
            return redirect(reverse('profile'))

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.author)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'cadmin/dashboard.html', context)


# def dashboard(request):
#     return render(request, 'cadmin/dashboard.html')