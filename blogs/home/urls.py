from django.urls import path
from . import views

app_name="home"

urlpatterns=[
    #home appp
    path('',views.index,name="home"),
    path('posts/<int:post_id>',views.post,name="post"),
    path('comment/<int:post_id>',views.comment,name="comment"),
    path('about/',views.about,name="about"),

    #blogger app
    path("blogger/dashboard/",views.dashboard,name="dashboard"),
    path("blogger/compose/",views.compose,name="compose"),
    path("blogger/edit/",views.edit,name="edit"),
    path("blogger/delete/",views.delete,name="delete"),
    path("blogger/edit/<int:post_id>/",views.editor,name="editor"),
    path("blogger/blog/points/",views.blog_points,name="blog_points"),
    path("blogger/theme/create/",views.create,name="create"),
    path("blogger/edit/theme/",views.editthemes,name="editthemes"),
    path("blogger/theme/editor/<int:theme_id>/",views.themeeditor,name="themeeditor"),

    #saved data app
    path("saved/data/blogs/",views.blogs,name="blogs"),
    path("saved/data/themes/",views.themes,name="themes"),
    path("saved/data/themes/<int:theme_id>",views.theme,name="theme"),
    path("blog/delete/single/notmorethanone/ghsdardasrhbsahvd/<int:post_id>/",views.delete_single,name="delete_single"),
    path("saved/data/comments/",views.comments_data,name="comments_data"),
    path('saved/data/comments/post/<int:post_id>/',views.comments_single_post,name="comments_single_post"),
    path("delete/theme/<int:theme_id>/",views.delete_theme,name="delete_theme"),
    path('saved/data/users',views.users,name="users"),

    #identity app
    path("login-signup/",views.login_signup,name="login_signup"),
    path("otp/<str:action>/",views.otpverification,name="otpverification"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login,name="login"),
    path("home/index/logout",views.logout,name="logout"),

    #redirect urls
    path("blog/posted/",views.blog_posted,name="blog_posted"),
    path("blogger/delete/blog/deleted/",views.delete_redirect,name="blog_deleted"),
    path("signup/successful/",views.signup_redirect,name="signup_redirect"),
    path("login/success",views.login_redirect,name="login_redirect"),
    path("theme/created/",views.createthemeredirect,name="theme_created"),
    path("theme/saved/<int:status>/",views.theme_saved,name="theme_saved"),
    path("blog/saved/",views.blog_saved,name="blog_saved")

]