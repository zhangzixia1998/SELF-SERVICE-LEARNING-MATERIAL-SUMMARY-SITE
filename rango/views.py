from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from datetime import datetime
from django.views import View
from rango.bing_search import run_query
def index(request):
    #request.session.set_test_cookie()
    context_dict = {}
    category_list = Category.objects.order_by('-likes')
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    # context_dict['pages'] = page_list
    visitor_cookie_handler(request)
    
    response = render(request, 'rango/index.html', context_dict)
    
    return response

def get_server_side_cookie(request,cookie,default_val=None):
    val = request.session.get(cookie)
    if not val:
        val=default_val
    return val
def visitor_cookie_handler(request):
    visits=int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit']=str(datetime.now())
    else:
        request.session['last_visit']=last_visit_cookie
    request.session['visits']=visits

def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/about.html', context_dict)
    
    return response
    

@login_required
def show_category(request, category_name_slug):
    context_dict = {}
    try:

        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category).order_by('-likes')

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:

        context_dict['category'] = None
        context_dict['pages'] = None
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            context_dict['result_list'] = run_query(query)
    
    return render(request, 'rango/category.html', context=context_dict)

   

@login_required
def add_category(request):
    form=CategoryForm()
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form': form})
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    if category is None:
        return redirect('/rango/')
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
    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']
            profile.save()
            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
'rango/register.html', {'user_form': user_form,
'profile_form': profile_form,
'registered': registered})

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request,'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))

@login_required
def like_page(request):
    page_id = None
    if request.method == 'GET':
        page_id = request.GET['page_id']
    likes = 0
    if page_id:
        page = Page.objects.get(id=int(page_id))
        if page:
            likes = page.likes + 1
            page.likes = likes
            page.save()
    return HttpResponse(page.likes)
@login_required
def dislike_page(request):
    page_id = None
    if request.method == 'GET':
        page_id = request.GET['page_id']
    dislikes = 0
    if page_id:
        page = Page.objects.get(id=int(page_id))
        if page:
            dislikes = page.dislikes + 1
            page.dislikes = dislikes
            page.save()
    return HttpResponse(page.dislikes)



class CategorySuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''
        category_list = get_category_list(max_results=8,starts_with=suggestion)
        if len(category_list) == 0:
            category_list = Category.objects.order_by('-likes')
        return render(request,'rango/categories.html', {'categories': category_list})

def get_category_list(max_results=0, starts_with=''):
    category_list = []
    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]
    return category_list
