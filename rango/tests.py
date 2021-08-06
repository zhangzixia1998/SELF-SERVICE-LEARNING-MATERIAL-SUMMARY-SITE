from django.test import TestCase
from django.urls import reverse
# Create your tests here.
from rango.models import Category
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        cat = Category(name='test',views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        cat = Category('Test Category Variables')
        cat.save()
        self.assertEqual(cat.slug, 'test-category-variables')



def add_cat(name, views=0, likes=0):
        cat = Category.objects.get_or_create(name=name)[0]
        cat.views = views
        cat.likes = likes
        cat.save()
        return cat
class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    
    def test_index_view_with_categories(self):
        add_cat('test1',1,1)
        add_cat('test2',1,1)
        add_cat('test3',1,1)
        add_cat('test4',1,1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test4")
        num_cats =len(response.context['categories'])
        self.assertEqual(num_cats , 4)