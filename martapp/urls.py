from django.urls import path
from . import views
from mart.settings import MEDIA_URL,MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('brands/',views.brands,name="brands"),
    path('products/',views.products,name="products"),
    path('see/<int:product_id>',views.see,name="see"),
    path('search/see/<int:product_id>',views.see,name="see"),
    path('products/see/<int:product_id>',views.see,name="see"),
    path('register/',views.register,name="register"),
    path('register',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('login',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('search/',views.search,name="search"),
    path('see/buy/<int:product_id>/',views.buy,name="buy"),
    path('see/buy/<int:product_id>',views.buy,name="buy"),
    path('search/see/buy/<int:product_id>',views.buy,name="buy"),
    path('products/see/buy/<int:product_id>/',views.buy,name="buy"),
    path('products/see/buy/<int:product_id>',views.buy,name="buy"),
    path('payment/verify',views.verifypayment,name="paymentverify"),
    path('orders/',views.orders,name="orders"),
    path('orders',views.orders,name="orders"),
    path('business/',views.business,name="business"),
    path('business',views.business,name="business"),
    path('businesslogin/',views.businesslogin,name="businesslogin"),
    path('businesslogin',views.businesslogin,name="businesslogin"),
    path('addproduct/',views.addproduct,name="addproduct"),
    path('addproduct',views.addproduct,name="addproduct"),
    path('myproducts/',views.myproducts,name="myproducts"),
    path('myproducts',views.myproducts,name="myproducts"),
    path('businesslogout/',views.businesslogout,name="businesslogout"),
    path('orderslist/',views.orderslist,name="orderslist"),
    path('orderslist',views.orderslist,name="orderslist")






] + static(MEDIA_URL,document_root=MEDIA_ROOT)