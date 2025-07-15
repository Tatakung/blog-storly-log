from django.urls import path
from blog import views
urlpatterns = [
    path('',views.index ,name='index' ) , 
    path('login', views.login_view, name='login'),        
    path('logout', views.logout_view, name='logout'),     
    path('register',views.register ,name='register' ) , 
    path('Home-Content',views.homeContent ,name='homecontent' ) , 
    path('Home-Content/user/<int:id>',views.homeContentUser ,name='homeContentUser' ) , 
    path('Home-Conten/My-contents',views.contentme ,name='contentme' ) , 
    path('Home-Conten/My-contents/<int:id>',views.contentmedetail ,name='contentmedetail' ) , 
    path('Home-Conten/My-contents/delete/<int:id>',views.contentmedelete ,name='contentmedelete' ) , 
    path('content/<int:id>/<str:content>',views.detail ,name='detail' ) , 
    path('content/submit/<int:id>',views.commented ,name='commented' ) , 
    path('content/delete/<int:id>',views.commenteddelete ,name='commenteddelete' ) , 
    
]