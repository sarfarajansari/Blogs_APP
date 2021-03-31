from django.db import models



# Create your models here.


class Feedback(models.Model):
    comment = models.CharField(max_length=999)
    def __str__(self):
        return f"{self.comment}"

class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    def __str__(self):
         return f"Name:{self.name},Email:{self.email}"


class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    comment = models.ForeignKey(Feedback,on_delete=models.CASCADE,related_name="commentby")
    comment_date=models.DateTimeField()
    def __str__(self):
        return f"{self.user},comment: {self.comment}"

class Paragraphs(models.Model):
    paragraph=models.CharField(max_length=99999)
    def __str__(self):
        return f"{self.paragraph}"
class fontstyles(models.Model):
    font=models.CharField(max_length=150)


class Gradient(models.Model):
    color1=models.CharField(max_length=50,default="")
    color2=models.CharField(max_length=50,default="")

class Theme(models.Model):
    title=models.CharField(blank=True,max_length=70,default="Theme")
    gradient=models.OneToOneField(Gradient,on_delete=models.CASCADE,blank=True,related_name="theme")
    textcolor=models.CharField(max_length=50,default="",blank=True)
    titlecolor=models.CharField(max_length=50,default="",blank=True)
    textfont=models.CharField(max_length=200,default="",blank=True)
    titlefont=models.CharField(max_length=200,default="",blank=True)

    def __str__(self):
        return self.title

    def edit(self,title,gradient,textcolor,titlecolor,textfont,titlefont):
        self.title=title
        self.gradient.delete()
        self.gradient=gradient

        self.textcolor=textcolor
        self.titlecolor=titlecolor
        self.textfont=textfont
        self.titlefont=titlefont
        self.save()
        return self

class defaultthemes(models.Model):
    theme=models.OneToOneField(Theme,on_delete=models.CASCADE,related_name="default")


class Article(models.Model):
    title = models.CharField(max_length=50)
    author=models.CharField(max_length=50)

    likes=models.IntegerField(default=-99999)
    comments = models.ManyToManyField(Comments,blank=True,related_name="post")
    content = models.ManyToManyField(Paragraphs,related_name="post",blank=True)
    shortcont= models.CharField(max_length=230,blank=True)
    theme=models.ManyToManyField(Theme,blank=True,related_name="post")
    posting_date=models.DateTimeField()
    def gettheme(self):
        theme=""
        for t in self.theme.all():
            theme=t
            return theme

    def get_blogger_name(self):
        name=self.blogger.get(id=1).user.name
        return name

    def shortcontent(self):
        if self.likes<0:
            self.shortcont=addshortcont(self)
            self.likes+=99999
            self.save()
    def comments_list_save(self):
        self.comments_list=self.comments.all()


    def __str__(self):
        return f"Title:{self.title} ,Author:{self.author}"


def addshortcont(post):
    for content in post.content.all():
        shortcont=""
        words= str(content).split()
        i=0
        for cont in words:
            shortcont+=cont+" "
            i+=1
            if i>34:

                return shortcont
        return shortcont





class Username(models.Model):
    username=models.CharField(max_length=70)
    def __str__(self):
        return f"@{self.username}"


class Blogger(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="blogger")
    password=models.CharField(max_length=30)
    article=models.ManyToManyField(Article,blank=True,related_name="blogger")
    title=models.CharField(max_length=30,default="blogger")
    Username=models.OneToOneField(Username,blank=False,related_name="blogger",on_delete=models.CASCADE)
    BP=models.IntegerField(default=0)
    theme=models.ManyToManyField(Theme,blank=True,related_name="blogger",default="")
    signup_date=models.DateTimeField()
    def calculate_BP(self):
        bp=0
        for post in self.article.all():
            bp+=10
            for comm in post.comments.all():
                bp+=4
        self.BP=bp
        return bp

    def dictinfo(self):
        name=self.user.name
        email=self.user.email
        password=self.password
        title=self.title
        username=self.Username.username
        id=self.id

        return {
            "name":name,
            "email":email,
            "password":password,
            "title":title,
            "username":username,
            "id":id
        }
    def __str__(self):
        return f" {self.user.name},{self.Username.username},{self.user.email} "



