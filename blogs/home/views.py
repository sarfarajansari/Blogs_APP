from django.shortcuts import render,redirect
from . models import*
from .authentication import sendotp
import random
import datetime
# views for reader app
def index(request,success="",error="",warning="",general=""):
    session=""
    posts= Article.objects.all()
    if "user" in request.session:
        session="session"
    for post in posts:
            post.shortcontent()


    return render(request,"home/index.html",{
        "posts":posts,
        "session":session,
        "success":success,
        "general":general,
        "error":error,
        "warning":warning
    })
#index created successfully




def post(request,post_id):
    post=Article.objects.get(pk=post_id)
    content= post.content.all()
    comments=post.comments.all()

    reader=""
    session=""
    blogger=""
    commentor=""
    if "user" in request.session:
        session="session"
        if request.session["user"]["title"] not in ["blogger","administrator"]:
            reader="role"
        else:
            blogger="role"
    elif "reader" in request.session:
        commentor="role"
    theme=""
    for t in post.theme.all():
        theme=t
        break

    return render(request,"home/posts.html",{
        "post":post,
        "content":content,
        "comments":comments,
        "session":session,
        "reader":reader,
        "blogger":blogger,
        "commentor":commentor,
        "reading_page":True,
        "theme":theme,


    })

def comment(request,post_id):

    blog=Article.objects.get(pk=post_id)
    if request.method=="POST":
        if "user" not in request.session and "reader" not in request.session:
            if "first_name" in request.POST and "last_name" in request.POST and "email" in request.POST:
                first_name = request.POST["first_name"]
                last_name=request.POST["last_name"]
                email = request.POST["email"]


                name= first_name + " "+ last_name
                reader={
                    "name":name,
                    "email":email,
                }
                request.session["reader"]=reader
            else:
                return redirect(f"/posts/{post_id}/")
        else:
            if "user" in request.session:
                user=User.objects.get(pk=request.session["user"]["id"])

            elif "reader" in request.session:
                user=User.objects.get(pk=request.session["reader"]["id"])

            if "comment" in request.POST:
                feedback= request.POST["comment"]
                feed=Feedback(comment=feedback)
                feed.save()
                date=datetime.datetime.now()
                comment=Comments(comment=feed,user=user,comment_date=date)
                comment.save()
                blog.comments.add(comment)
                blog.save()

            return redirect(f"/posts/{post_id}")


        if "comment" in request.POST:
            feedback= request.POST["comment"]
        user=User(name=name,email=email)

        user.save()
        if "reader" in request.session:
            request.session["reader"]["id"]=user.id
        feed=Feedback(comment=feedback)
        feed.save()
        date=datetime.datetime.now()
        comment=Comments(comment=feed,user=user,comment_date=date)
        comment.save()
        blog.comments.add(comment)
        blog.save()



        return redirect(f"/posts/{post_id}")

    else:
        return redirect(f"/posts/{post_id}")


def about(request):

    return render(request,"home/about.html",{
        "session":"session"
    })



# blogger app views
def dashboard(request,success="",error="",warning="",general=""):
    if "user" in request.session:
        blogger=""
        administrator=""
        role=request.session["user"]["title"]
        if role in ["blogger","administrator"]:
            if role=="blogger":
                blogger="role"
            else:
                administrator="role"


            posts=list(Blogger.objects.get(id=request.session["user"]["id"]).article.all())
            no_of_posts=len(posts)
            no_of_comments=0
            for post in posts:
                no_of_comments+=len(list(post.comments.all()))

            BP=Blogger.objects.get(pk=request.session["user"]["id"]).calculate_BP()
            return render(request,"composer/dashboard.html",{
                "blogger":blogger,
                "administrator":administrator,
                "error":error,
                "general":general,
                "warning":warning,
                "success":success,
                "no_of_posts":no_of_posts,
                "username":request.session["user"]["username"],
                "no_of_comments":no_of_comments,
                "BP":BP
            })
    return index(request,warning="You haven't signed up , please sign up first!")

def compose(request):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                defaulttheme=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="blogger":
                        blogger="role"
                        themes=Blogger.objects.get(pk=request.session["user"]["id"]).theme.all()
                        defaulttheme=defaultthemes.objects.all()
                    else:
                        administrator="role"
                        themes=Theme.objects.all()
                        defaulttheme=""

                    rangelist = [2,3,4,5,6,7,8,9,10,11,12,13,14,15]
                    if request.method=="GET":

                        return render(request,"composer/compose.html",{
                            "rangelist":rangelist,
                            "author":request.session["user"]["name"],
                            "blogger":blogger,
                            "administrator":administrator,
                            "defaultthemes":defaulttheme,
                            "themes":themes
                        })
                    elif request.method=="POST":
                        if "title" in request.POST and "author" in request.POST:
                            title=request.POST["title"]
                            author=request.POST["author"]
                            date=datetime.datetime.now()
                            post=Article(title=title,author=author,posting_date=date)
                            para=Paragraphs(paragraph= request.POST["1"])
                            para.save()
                            post.save()
                            post.content.add(para)
                            for i in rangelist:
                                if str(request.POST[str(i)]):
                                    para=Paragraphs(paragraph=request.POST[str(i)])
                                    para.save()
                                    post.content.add(para)
                                    post.save()
                            post.save()
                            if "theme" in request.POST:
                                if request.POST["theme"]!="":
                                    post.theme.add(Theme.objects.get(pk=request.POST["theme"]))
                                    post.save()

                            blogger=Blogger.objects.get(pk=request.session["user"]["id"])
                            blogger.article.add(post)
                            blogger.save()
                            return redirect('/blog/posted' )

                        else:
                            return dashboard(request,error="not enough information given")




    return index(request,warning="You haven't signed up , please sign up to compose blogs!")
def blog_posted(request):
    return dashboard(request,success="blog posted",general="Congrats you received 10BP")

def delete(request):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                posts=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        administrator="role"
                        posts=Article.objects.all()
                    else:
                        blogger="role"
                        posts=Blogger.objects.get(pk=request.session["user"]["id"]).article.all()


                    if request.method=="GET":
                        return render(request,"composer/delete.html",{
                            "posts":posts,
                            "administrator":administrator,
                            "blogger":blogger
                        })
                    if request.method=="POST":
                        for post in posts:
                            key=str(post.id)
                            if key in request.POST:
                                post.delete()
                        return redirect("blog/deleted")
    return index(request,warning="You haven't signed up , please sign up first!")

def delete_redirect(request):
    if "user" and "status" in request.session:
        if request.session["status"]=="verified":
            blogger=""
            administrator=""
            posts=""
            role=request.session["user"]["title"]
            if role=="administrator":
                administrator="role"
                posts=Article.objects.all()
            else:
                blogger="role"
                posts=Blogger.objects.get(pk=request.session["user"]["id"]).article.all()
            return render(request,"composer/delete.html",{
                                    "posts":posts,
                                    "administrator":administrator,
                                    "blogger":blogger,
                                    "general":"Blog deleted"
                                })
    dashboard(request)


def delete_single(request,post_id):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                if request.session["user"]["title"]=="blogger":
                    user_blogs= Blogger.objects.get(pk=request.session["user"]["id"]).article.all()

                    for post in user_blogs:
                        if post_id==post.id:
                            post.delete()
                            return blogs(request,success="blog deleted")
                    return blogs(request,error="couldn't find the blog!")
                elif request.session["user"]["title"]=="administrator":
                    if post_id in list(Article.objects.values_list("id",flat=True)):
                        post=Article.objects.get(pk=post_id)
                        post.delete()
                        return blogs(request,success="Blog deleted!")
                    else:
                        return blogs(request,error="Could'nt find blog")

                else:
                    return dashboard(request,error="some error occured")

    return index(request,warning="You haven't signed up , please sign up first!")






def edit(request,success="",error=""):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                posts=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="blogger":
                        blogger="role"
                        posts=Blogger.objects.get(pk=request.session["user"]["id"]).article.all()
                    else:
                        administrator="role"
                        posts=Article.objects.all()

                    return render(request,"composer/edit.html",{
                            "posts":posts,
                            "blogger":blogger,
                            "administrator":administrator,
                            "success":success,
                            "error":error
                        })
    return index(request,warning="You haven't signed up , please sign up first!")

def editor(request,post_id):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                post=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        themes=Theme.objects.all()
                        defaulttheme=""

                        administrator="role"
                        post=Article.objects.get(pk=post_id)


                    else:
                        themes=Blogger.objects.get(pk=request.session["user"]["id"]).theme.all()
                        defaulttheme=defaultthemes.objects.all()
                        blogger="role"
                        for blog in Blogger.objects.get(pk=request.session["user"]["id"]).article.all():
                            if blog.id==post_id:
                                post=blog
                    if post=="":
                        return dashboard(request,error="blog not found")




                    rangelist = [2,3,4,5,6,7,8,9,10,11,12,13,14,15]

                    if request.method=="GET":
                        paragraphs=list(post.content.all())
                        n=len(paragraphs)
                        for i in range(2,n+1):
                            if i in rangelist:
                                rangelist.remove(i)

                        return render(request,"composer/editor.html",{
                            "currenttheme":post.gettheme(),
                            "post":post,
                            "rangelist":rangelist,
                            "index":n+1,
                            "paragraphs":paragraphs,
                            "blogger":blogger,
                            "administrator":administrator,
                            "defaultthemes":defaulttheme,
                            "themes":themes
                        })
                    elif request.method=="POST":
                        for para in post.content.all():
                            para.delete()
                        post.save()



                        if "author" in request.POST and "title" in request.POST:
                            post.title=request.POST["title"]
                            post.author=request.POST["author"]
                            post.save()




                        para=Paragraphs(paragraph= request.POST["1"])
                        para.save()
                        post.save()
                        post.content.add(para)
                        for i in rangelist:
                            if str(request.POST[str(i)]):
                                para=Paragraphs(paragraph=request.POST[str(i)])
                                para.save()
                                post.content.add(para)
                                post.save()
                        post.save()
                        if "theme" in request.POST:
                            if request.POST["theme"]!="":
                                post.theme.clear()

                                post.theme.add(Theme.objects.get(pk=request.POST["theme"]))
                                post.save()

                        paragraphs=list(post.content.all())
                        n=len(paragraphs)
                        for i in range(2,n+1):
                            if i in rangelist:
                                rangelist.remove(i)

                        return redirect(f"/blog/saved")
    return dashboard(request)

def blog_saved(request):
    return edit(request,success="blog saved")

def blogs(request,success="",error="",warning="",general=""):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                blogs=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        administrator="role"
                        blogs=Article.objects.all()
                    else:
                        blogger="role"
                        blogs=Blogger.objects.get(pk=request.session["user"]["id"]).article.all()

                    return render(request,"saved_data/blogs.html",{
                        "posts":blogs,
                        "administrator":administrator,
                        "blogger":blogger,
                        "error":error,
                        "general":general,
                        "warning":warning,
                        "success":success
                    })
    return dashboard(request)

def themes(request,success="",error="",warning="",general=""):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                blogs=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        administrator="role"
                        themes=Theme.objects.all()
                    else:
                        blogger="role"
                        themes=Blogger.objects.get(pk=request.session["user"]["id"]).theme.all()

                    return render(request,"saved_data/themes.html",{
                        "themes":themes,
                        "administrator":administrator,
                        "blogger":blogger,
                        "error":error,
                        "general":general,
                        "warning":warning,
                        "success":success
                    })
    return dashboard(request)

def delete_theme(request,theme_id):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                if request.session["user"]["title"]=="blogger":
                    user_themes= Blogger.objects.get(pk=request.session["user"]["id"]).theme.all()

                    for theme in user_themes:
                        if theme_id==theme.id:
                            theme.delete()
                            return themes(request,success="theme deleted")

                    return themes(request,error="couldn't find the theme!")
                elif request.session["user"]["title"]=="administrator":
                    if theme_id in list(Theme.objects.values_list("id",flat=True)):
                        theme=Theme.objects.get(pk=theme_id)
                        theme.delete()
                        return themes(request,success="theme deleted!")
                    else:
                        return themes(request,error="Could'nt find theme")

                else:
                    return dashboard(request,error="some error occured")

    return index(request,warning="You haven't signed up , please sign up first!")

def theme(request,theme_id,success="",error="",warning="",general=""):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                theme=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        administrator="role"
                        theme=Theme.objects.get(pk=theme_id)
                        return render(request,"saved_data/theme.html",{
                        "theme":theme,
                        "administrator":administrator,
                        "blogger":blogger,
                        "error":error,
                        "general":general,
                        "warning":warning,
                        "success":success
                    })
                    else:
                        blogger="role"
                        themes=Blogger.objects.get(pk=request.session["user"]["id"]).theme.all()
                        for i in themes:
                            if i.id==theme_id:
                                theme=i
                                return render(request,"saved_data/theme.html",{
                                "theme":theme,
                                "administrator":administrator,
                                "blogger":blogger,
                                "error":error,
                                "general":general,
                                "warning":warning,
                                "success":success
                                })
                        return render(request,"saved_data/theme.html",{
                        "theme":theme,
                        "administrator":administrator,
                        "blogger":blogger,
                        "error":"Theme not found!",
                        "general":general,
                        "warning":warning,
                        "success":success
                    })


    return dashboard(request)


def create(request,success="",error="",warning="",general=""):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        administrator="role"
                    else:
                        blogger="role"

                    if request.method=="GET":
                        return render(request,"composer/theme.html",{
                        "administrator":administrator,
                        "blogger":blogger,
                        "fontstyle":fontstyles.objects.all(),
                        "lists":["title","content"]
                    })
                    else:
                        if "color1" in request.POST and "color2" in request.POST and "titlefont" in request.POST and "contentfont" in request.POST and "titlecolor" in request.POST and "contentcolor" in request.POST and "title" in request.POST:
                            P=request.POST
                            gradient=Gradient(color1=P["color1"],color2=P["color2"])
                            gradient.save()
                            theme=Theme(
                                title=P["title"],
                                gradient=gradient,
                                textcolor=P["contentcolor"],
                                titlecolor=P["titlecolor"],
                                textfont=P["contentfont"],
                                titlefont=P["titlefont"]
                                )
                            theme.save()
                            user=Blogger.objects.get(pk=request.session["user"]["id"])
                            user.theme.add(theme)
                            user.save()
                            return redirect("/theme/created")



    return dashboard(request)

def createthemeredirect(request):
    return dashboard(request,success="Theme created!You can use it in your posts now!")


def users(request):
    administrator=""
    blogger=""
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                if request.session["user"]["title"]=="administrator":
                    administrator="role"
                    bloggers=Blogger.objects.all()
                    return render(request,"saved_data/users.html",{
                        "bloggers":bloggers,
                        "administrator":administrator,
                        "blogger":blogger
                    })
    return index(request)


def comments_data(request):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                blogs=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        administrator="role"
                        blogs=Article.objects.all()
                    else:
                        blogger="role"
                        blogs=Blogger.objects.get(pk=request.session["user"]["id"]).article.all()


                    for post in blogs:
                        post.comments_list_save()
                        post.save()
                    return render(request,"saved_data/comments.html",{
                        "posts":blogs,
                        "administrator":administrator,
                        "blogger":blogger
                    })
    return dashboard(request)



def comments_single_post(request,post_id):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                blogs=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        administrator="role"

                    else:
                        blogger="role"

                    post=""
                    for blog in Article.objects.all():
                        if blog.id==post_id:
                            post=blog
                    if post=="":
                        #alert making work left
                        return dashboard(request,error="Post Not Found")
                    post.comments_list_save()
                    posts=[post]
                    return render(request,"saved_data/comments.html",{
                        "posts":posts,
                        "administrator":administrator,
                        "blogger":blogger
                    })
    return dashboard(request)


def login_signup(request):

    if "user" not in request.session:
            return render(request,"identity/login_signup.html"
            )

    return dashboard(request)

def otpverification(request,action):
    if request.method=="POST":
        if action=="verify":
            if "otp" in request.POST and "otp" in request.session and "status" in request.session:
                if request.session["status"]=="unverified":
                    if str(request.POST["otp"])==str(request.session["otp"]):
                        request.session["status"]="verified"
                        return redirect("/signup")
                        #alert
                    else:
                        #alter
                        return render(request,"identity/otp.html",{
                            "error":"incorect OTP,Try resending!",
                            "email":request.session["email"]
                        })
                else:
                    #alert
                    return dashboard(request,general="Email already verified")
        elif action=="send":
            if "email" in request.POST:
                email= request.POST["email"]
                request.session["email"]=email
                otp=random.randint(100001,999999)
                print(otp,"\n\n")
                print(email)
                request.session["otp"]=otp
                sendotp(email,otp)
                print("sentt")
                request.session["status"]="unverified"
                return render(request,"identity/otp.html",{
                    "email":email,
                    "success":"OTP sent"
                })

    return render(request,"identity/otp.html")

def signup(request):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if request.method=="POST":
                if "username" in request.POST and "email" in request.session and "password" in request.POST and "name" in request.POST:
                    username=request.POST["username"].lower()
                    for uname in Username.objects.all():
                        if username==str(uname.username):
                            return render(request,"identity/signup.html",{
                                "error":"Username Unavailable,Please try a diffrent one!"
                            })

                    name=request.POST["name"]
                    email=request.session["email"]
                    password=request.POST["password"]



                    user=User(name=name,email=email)
                    uname=Username(username=username)
                    user.save()
                    uname.save()
                    date=datetime.datetime.now()

                    blogger=Blogger(user=user,Username=uname,password=password,signup_date=date)
                    blogger.save()
                    request.session["user"]=blogger.dictinfo()
                    return redirect("/signup/successful")

                else:
                    return render(request,"identity/signup.html",{
                                "error":"Invalid information sent"
                            })
            elif request.method=="GET":

                return render(request,"identity/signup.html")


    return render(request,"identity/otp.html")

def signup_redirect(request):
    return dashboard(request,success="You've signed up successfully",general="welcome to the YOUTH BLOG,We're happy to have you:),start showing your creative writings!!")




def login(request):
    if "user" not in request.session:
        if request.method=="POST":
            username=request.POST["username"]
            password=request.POST["password"]
            for user in Blogger.objects.all():
                if user.Username.username==username:
                    if user.password==password:
                        request.session["user"]= user.dictinfo()
                        request.session["status"]="verified"
                        return redirect("/login/success")

            return render(request,"identity/login.html",{
                "error":"Invalid username or password!"
            })

        if request.method=="GET":
            return render(request,"identity/login.html")


    return dashboard(request,general="You have already logged in!!")

def login_redirect(request):
    return dashboard(request,success="Logged in successfully!",general="Welcome back !! We are glad to have you:)")

def logout(request):
    if "user" in request.session:
        try:
            del request.session['user']
        except  KeyError:
            pass


        posts= Article.objects.all()
        for post in posts:
            post.shortcontent()

        return render(request,"home/index.html",{
            "success":"logged out successfully",
            "posts":posts
        })
    return index(request)

def blog_points(request):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                role=request.session["user"]["title"]
                if role=="blogger":
                        blogger="role"
                else:
                    administrator="role"
                if request.session["status"]=="verified":
                    user=Blogger.objects.get(pk=request.session["user"]["id"])



                    return render(request,"composer/blog_points.html",{
                            "BP":user.calculate_BP(),
                            "administrator":administrator,
                            "blogger":blogger
                        })
    return dashboard(request)


def editthemes(request,error="",success=""):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                blogs=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        administrator="role"
                        themes=Theme.objects.all()
                    else:
                        blogger="role"
                        themes=Blogger.objects.get(pk=request.session["user"]["id"]).theme.all()

                    return render(request,"composer/edittheme.html",{
                        "themes":themes,
                        "administrator":administrator,
                        "blogger":blogger,
                        "error":error,
                        "success":success
                    })
    return dashboard(request)


def themeeditor(request, theme_id ):
    if "status" in request.session:
        if request.session["status"]=="verified":
            if "user" in request.session:
                blogger=""
                administrator=""
                theme=""
                role=request.session["user"]["title"]
                if role in ["blogger","administrator"]:
                    if role=="administrator":
                        administrator="role"
                        theme=Theme.objects.get(pk=theme_id)
                    else:
                        blogger="role"
                        themes=Blogger.objects.get(pk=request.session["user"]["id"]).theme.all()
                        for t in themes:
                            if t.id==theme_id:
                                theme=t
                                break
                    if request.method=="GET":
                        return render(request,"composer/themeeditor.html",{
                            "theme":theme,
                            "administrator":administrator,
                            "blogger":blogger,
                            "fontstyle":fontstyles.objects.all()
                        })
                    else:
                        P=request.POST
                        if "color1" in P and "color2" in P and "titlefont" in P and "contentfont" in P and "titlecolor" in P and "contentcolor" in P and "title" in P:

                            gradient=Gradient(color1=P["color1"],color2=P["color2"])
                            gradient.save()
                            for i in P:
                                print(i,P[i],"\n")
                            theme=theme.edit(P["title"],gradient,P["contentcolor"],P["titlecolor"],P["contentfont"],P["titlefont"]
                                )
                            user=Blogger.objects.get(pk=request.session["user"]["id"])
                            user.theme.add(theme)
                            user.save()
                            return redirect("/theme/saved/1")
                        return redirect("/theme/saved/2")

    return dashboard(request)

def theme_saved(request,status):
    if status==1:
        return editthemes(request,success="Theme saved")
    elif status==0:
        return editthemes(request,error="invalid information given")
    else:
        dashboard(request)




