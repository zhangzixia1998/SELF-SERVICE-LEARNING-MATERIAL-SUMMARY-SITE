import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

# For an explanation of what is going on here, please refer to the TwD book.

def populate():
    css_pages = [
        {'title': 'CSS Tutorial',
         'url':'https://www.w3schools.com/css/',
         'views': 44,},
        {'title':'CSS Tricks',
         'url':'https://css-tricks.com/a-step-by-step-process-for-turning-designs-into-code/',
         'views': 93},
        ]
    
    js_pages = [
        {'title':'JavaScript Tutorial',
         'url':'https://www.w3schools.com/js/',
         'views': 302},
        {'title':'JavaScript Community',
         'url':'https://www.javascript.com/resources',
         'views': 172},
        ]
    ajax_pages = [
        {'title': 'AJAX Tutorial',
         'url':'https://www.w3schools.com/xml/ajax_intro.asp',
         'views': 44,},
        {'title':'AJAX tricks',
         'url':'http://www.dhtmlgoodies.com/',
         'views': 93},
        ]
    cats = {'css': {'pages': css_pages, 'views': 128, 'likes': 64},
            'js': {'pages': js_pages, 'views': 64, 'likes': 32},
            'ajax': {'pages': ajax_pages, 'views': 10, 'likes': 20},
        }
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()