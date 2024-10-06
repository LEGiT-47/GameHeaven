from django.urls import path
from shop import views

# user grocery_user  pass : grocery123

urlpatterns = [
    path('', views.home, name='home'),
    # path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    # path('product/', views.product, name='product'),
    # path('review/', views.review, name='review'),
    # path('blog/', views.blog, name='blog'),
    # path('check-in/', views.check_in, name='check_in'),
    # path('cart/', views.shopping_cart, name='shopping_cart'),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('checkout/', views.checkout, name='checkout'),
    path('mycart/', views.mycart, name='mycart'),
    path('add/<int:product_id>/', views.add, name='add'),
    path("contact/", views.contact, name='contact'),
    path('products/',views.products,name="products"),
    path('homeret/',views.homeret,name="homeret"),
    path('slim/',views.slim,name="slim"),
    path('search/',views.search,name="search"),
]
