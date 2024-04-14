from django.core.mail import send_mail
import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decouple import config

from gramm.constants import ACTIVATION_EMAIL_SUBJECT, ACTIVATION_EMAIL_MESSAGE
from gramm.forms import CustomUserEditForm, PostForm, ImageFormSet, CustomUserCreationForm, CustomAuthenticationForm
from gramm.models import Post, Like, Tag, Subscription


def home_page(request):
    """
        Render the home page with user information.
        :param request: HTTP request object
        :return: Rendered home page HTML
        """
    context = {'user': request.user}
    return render(request, 'home_page.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = str(uuid.uuid4())
            user.profile_activation_token = token
            user.save()

            activation_link = request.build_absolute_uri(reverse('gramm:profile', args=[user.id]))
            subject = ACTIVATION_EMAIL_SUBJECT
            message = ACTIVATION_EMAIL_MESSAGE.format(activation_link=activation_link)
            from_email = config('EMAIL_HOST_USER')
            to_email = [user.email]

            send_mail(subject, message, from_email, to_email, fail_silently=False)

            return redirect('gramm:activation_info')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def activation_info(request):
    """
        Render activation information.

        :param request: HTTP request object
        :return: Rendered activation information HTML
        """
    return render(request, 'activation_info.html')


def login_view(request):
    """
        Handle user login.
        :param request: HTTP request object
        :return: Rendered login HTML
        """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('gramm:profile', args=[user.id]))
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


def social_login_success(request, backend, user, *args, **kwargs):
    """
    Handle successful social login.

    :param request: HTTP request object
    :param backend: Backend that handled the login
    :param user: User object
    :param args: Additional positional arguments
    :param kwargs: Additional keyword arguments
    :return: Redirect to user profile page
    """

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect(reverse('gramm:profile', args=[user.id]))


def logout_view(request):
    """
    Handle user logout.
    :param request: HTTP request object
    :return: Redirect to home page after logout
    """
    logout(request)
    return redirect('gramm:home_page')


def profile(request, user_id):
    user = get_user_model().objects.filter(id=user_id).first()

    followers = Subscription.objects.filter(following=user).select_related('follower')
    following = Subscription.objects.filter(follower=user).select_related('following')

    posts = Post.objects.filter(user=user).prefetch_related('tags')

    is_following_user = False
    if request.user.is_authenticated:
        is_following_user = Subscription.objects.filter(follower=request.user, following=user).exists()

    is_own_profile = (user == request.user)

    if is_own_profile:
        is_following_user = False

    return render(request, 'profile.html', {
        'user': user,
        'followers': followers,
        'following': following,
        'posts': posts,
        'is_following_user': is_following_user,
        'is_own_profile': is_own_profile,
    })


def edit_profile(request, user_id):
    """
    Handle user profile editing.
    :param request: HTTP request object
    :param user_id: User ID for the profile to be edited
    :return: Rendered edit profile HTML
    """
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('gramm:profile', user_id=user.id)
    else:
        form = CustomUserEditForm(instance=user)

    context = {'user': user, 'form': form}
    return render(request, 'edit_profile.html', context)


def create_post(request):
    """
    Handle the creation of a new post, including form validation and image uploading.

    :param request: HTTP request object
    :return: Rendered create post HTML
    """
    user = request.user

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=Post())

        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save(commit=False)
            post.user = user
            post.save()

            tags_raw = post_form.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tags_raw.split(',') if tag.strip()]
            for tag_name in tags_list:
                tag_name = tag_name.lstrip('#')
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            images = image_formset.save(commit=False)
            for image in images:
                image.post = post
                image.save()

            messages.success(request, 'Post created successfully!')
            return redirect('gramm:profile', user_id=user.id)
    else:
        post_form = PostForm()
        image_formset = ImageFormSet(instance=Post())

    return render(request, 'create_post.html',
                  {'post_form': post_form, 'image_formset': image_formset, 'user': user})


def delete_post(request, post_id):
    """
        Handle post deletion.
        :param request: HTTP request object
        :param post_id: ID of the post to be deleted
        :return: Redirect to user profile with appropriate message
        """
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.user:
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    else:
        messages.error(request, 'You do not have permission to delete this post.')

    return redirect('gramm:profile', user_id=request.user.id)


def like_post(request, post_id):
    """
    Handle liking/unliking a post.
    :param request: HTTP request object
    :param post_id: ID of the post to be liked/unliked
    :return: Redirect to user profile after processing the like
    """
    post = get_object_or_404(Post, id=post_id)

    if Like.objects.filter(user=request.user, post=post).exists():
        Like.objects.filter(user=request.user, post=post).delete()

    return redirect('profile', user_id=request.user.id)


def tag_posts(request, tag_name):
    """
        Display posts associated with a specific tag.
        :param request: HTTP request object
        :param tag_name: Name of the tag to filter posts
        :return: Rendered tag posts HTML
        """
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag).select_related('user')
    context = {'tag': tag, 'posts': posts}
    return render(request, 'tag_posts.html', context)


def manage_subscription(request, user_id, action):
    """
    Manage user subscriptions (subscribe, unsubscribe, followers list).

    :param request: HTTP request object
    :param user_id: User ID for the subscription management
    :param action: Action to perform (subscribe, unsubscribe, followers)
    :return: Rendered HTML or redirect based on the action
    """
    user_to_manage = get_object_or_404(get_user_model(), id=user_id)

    if action == 'subscribe' and not Subscription.objects.filter(follower=request.user,
                                                                 following=user_to_manage).exists():

        Subscription.objects.create(follower=request.user, following=user_to_manage)
    elif action == 'unsubscribe':

        Subscription.objects.filter(follower=request.user, following=user_to_manage).delete()
    elif action == 'followers':

        followers = Subscription.objects.filter(following=user_to_manage).select_related('follower')
        return render(request, 'followers_list.html', {'user_to_manage': user_to_manage, 'followers': followers})
    else:

        return HttpResponseBadRequest("Invalid action")

    return redirect('profile', user_id=user_id)
