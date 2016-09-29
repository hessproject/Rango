from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from rango.models import Page, Category
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# Create your views here.

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list,
                    'pages': pages_list}

    return render(request, 'rango/index.html',context=context_dict)


def about(request):
    context_dict = {'authorname': "Nick Hess"}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all associated pages. Filter returns list of page objects or empty list
        pages = Page.objects.filter(category=category)
        context_dict["pages"] = pages
        context_dict["category"] = category

    except Category.DoesNotExist:
        context_dict["pages"] = None
        context_dict["category"] = None

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    #Changed to true if registration is successful
    registered = False

    if request.method == 'POST':
        # Attempt to grab information from form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # set_password method hashes raw password
            user.set_password(user.password)
            user.save()

            #commit false delays sending the model to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        # Not an HTTP POST, so we render form using two ModelForm instances.
        # They will be blank, ready for user input

        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered}
    return render(request,'rango/register.html', context_dict)


def user_login(request):

    if request.method == 'POST':
        # use POST.get vs POST[variable] because get returns none if the value doesn't exist
        # while the other method will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        # There will be a user object if details from before are correct
        if user:
            # Check if account is active or disabled
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your Rango account is disabled.')
        else:
            print("Invalid login details: {0},{1}".format(username, password))
            return render('Invalid login details supplied.')

    else:
        return render(request, 'rango/user_login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def restricted(request):
    return HttpResponse('You can see this text if you are logged in')

