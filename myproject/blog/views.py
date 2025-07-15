from django.shortcuts import render,redirect , get_object_or_404
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from blog.models import Blog,Comment
from category.models import Category
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
def index(request):
    category = Category.objects.all()
    poppular = Blog.objects.all().order_by('-views')[:10]

    blog = Blog.objects.all()  # เริ่มจาก query set ทั้งหมด
    valueType = 'ทั้งหมด'

    if request.method == "GET":
        Namecategory = request.GET.get('category')
        Namearticle = request.GET.get('article')

        if Namecategory:
            valueType = Namecategory
            typecategory = Category.objects.filter(name=Namecategory).first()
            if typecategory:
                blog = blog.filter(category=typecategory.id)
            else:
                valueType = 'ทั้งหมด'

        if Namearticle:
            blog = blog.filter(
                Q(name__icontains=Namearticle) | Q(content__icontains=Namearticle)
            )

    return render(request, 'blog.html', {
        'category': category,
        'blog': blog,
        'valueType': valueType,
        'poppular': poppular,
    })

def detail(request,id,content) :
    blog = get_object_or_404(Blog,id=id)
    test = Comment.objects.filter(blog = blog)
    blog.views += 1
    blog.save()  
    return render(request,'detail.html',{'blog' : blog , 'joy' : test}) ; 
# คอมเม้น
def commented(request, id):
    if request.method == "POST":
        comment = request.POST.get('comment')
        blog = get_object_or_404(Blog, id=id)
        if not comment:
            # messages.error(request, "กรุณาใส่ข้อความก่อนส่ง")
            return redirect('detail', id=blog.id, content=blog.name)
        if request.user.is_authenticated:
            Comment.objects.create(
                content=comment,
                customer=request.user,
                blog=blog
            )
        return redirect('detail', id=blog.id, content=blog.name)

    return redirect('detail', id=id, content=get_object_or_404(Blog, id=id).name)


def commenteddelete(request,id) : 
    comment = get_object_or_404(Comment, id=id)

    if request.user == comment.customer:
        comment.delete()
   

    return redirect('detail', id=comment.blog.id, content=comment.blog.name)
    



def login_view(request):
    if request.user.is_authenticated:
        return redirect('homecontent')  
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homecontent')
        else:
            messages.warning(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render(request, 'login.html')

def register(request) :
    if request.user.is_authenticated:
        return redirect('homecontent')  
    if request.method == 'POST' :
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = email  
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.warning(request, "รหัสผ่านไม่ตรงกัน")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.warning(request, "มีอีเมลนี้ในระบบแล้ว")
            return redirect('register')
        # สร้าง user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)  
        return redirect('homecontent')  
    return render(request,'register.html')
def logout_view(request):
    logout(request) 
    return redirect('login') 
@login_required(login_url='login')
def homeContent(request):
    category = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        content = request.POST.get('content')
        category_id = request.POST.get('type')
        image = request.FILES.get('image')  # รับไฟล์จาก form

        # ตรวจสอบความถูกต้อง
        if not name or not content or not category_id:
            messages.success(request, "กรุณากรอกข้อมูลให้ครบถ้วน")
            return redirect('homecontent')
        # สร้างบทความ
        blog = Blog.objects.create(
            name=name,
            content=content,
            category=Category.objects.get(id=category_id),
            image=image,
            customer=request.user  # ผู้ใช้ที่เข้าสู่ระบบ
        )
        messages.success(request, "เพิ่มบทความเรียบร้อยแล้ว")
        return redirect('homecontent')

    return render(request, 'user-content.html', {'category': category})
def homeContentUser(request , id ) :
    user = get_object_or_404(User,id=id)
    blog = Blog.objects.filter(customer=user)
    return render(request,'portdetail.html',{'blog' : blog , 'user' : user})
def contentme(request) :
    if not request.user.is_authenticated:
        # หากผู้ใช้ยังไม่ได้ล็อกอิน
        return redirect('login')
    blogMe = Blog.objects.filter(customer=request.user).order_by('-id')
    return render(request,'contentme.html',{'blogMe':blogMe})

def contentmedelete(request, id):
    blog = get_object_or_404(Blog, id=id, customer=request.user)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "ลบบทความเรียบร้อยแล้ว")
        return redirect('contentme')

    # ถ้าไม่ได้ POST ให้ redirect กลับ
    return redirect('contentme')

def contentmedetail(request, id):
    blog = get_object_or_404(Blog, id=id, customer=request.user)  # ปลอดภัยกว่าใช้ .filter().first()
    category = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        content = request.POST.get('content')
        category_id = request.POST.get('type')
        image = request.FILES.get('image')  # ไม่จำเป็นต้องอัปโหลดใหม่ทุกครั้ง

        # ตรวจสอบความถูกต้อง
        if not name or not content or not category_id:
            messages.error(request, "กรุณากรอกข้อมูลให้ครบถ้วน")
            return redirect('contentmedetail', id=id)

        blog.name = name
        blog.content = content
        blog.category = Category.objects.get(id=category_id)
        if image:
            blog.image = image  # อัปเดตเฉพาะเมื่อมีไฟล์ใหม่
        blog.save()

        messages.success(request, "อัปเดตบทความเรียบร้อยแล้ว")
        return redirect('contentme')

    return render(request, 'contentdetail.html', {
        'data': blog,
        'category': category
    })