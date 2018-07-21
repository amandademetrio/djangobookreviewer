from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import *
from django.contrib import messages

#Loading pages

def index(request):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'reviews':Review.objects.all().order_by('-id')[:3][::-1],
            'books':Book.objects.all()
        }
        return render(request,'first_app/success.html',context)
    else:
        return render(request,'first_app/index.html')

def addbook(request):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'authors':Author.objects.all(),
            'books':Book.objects.all()
        }
        return render(request,'first_app/addbook.html',context)
    else:
        return redirect('/')

def loadbook(request,number):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'book':Book.objects.get(id=number),
            'reviews':Review.objects.filter(related_book=number)
        }
        return render(request,'first_app/bookpage.html',context)
    else:
        return redirect('/')

def loaduser(request,number):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'reviews':Review.objects.filter(commentator=number),
            'count':Review.objects.filter(commentator=number).count()
        }
        return render(request,'first_app/userpage.html',context)
    else:
        return redirect('/')

#Processing info
def registration(request): #Handles registration process and sets up session with information
    errors = User.objects.basic_validator(request.POST)

    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags='registration_errors')
        return redirect('/')
    
    else:
        new_user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        new_user.save()
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        request.session['email'] = new_user.email
        request.session['logged_in'] = True
        request.session['user_id'] = new_user.id
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    
    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags='login_errors')
        return redirect('/')
    
    else:
        login_user = User.objects.get(email=request.POST['email'])
        request.session['first_name'] = login_user.first_name
        request.session['last_name'] = login_user.last_name
        request.session['email'] = login_user.email
        request.session['logged_in'] = True
        request.session['user_id'] = login_user.id
        return redirect('/')

def processaddbook(request):
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)

        if len(errors):
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/books/add')
    
        else:
            book_title = request.POST['new_title']
            current_user = User.objects.get(id=request.session['user_id'])
            book_rating = int(request.POST['ratings'])
            
            #Getting book author
            if len(request.POST['regular_author']) < 2:
                book_author = Author.objects.create(name=request.POST['new_author'])
            else:
                book_author = Author.objects.filter(name=request.POST['regular_author'])[0]
            
            new_book = Book.objects.create(name=book_title,author=book_author,uploader=current_user)

            new_review = Review.objects.create(content=request.POST['book_review'],commentator=current_user,related_book=new_book,ratings=book_rating)

            request.session['current_book'] = new_book.id

            #prevent user from sending repeat books and authors
            return redirect(loadbook,number=new_book.id)

def processaddreview(request):
    if request.method == "POST":
        book_id = request.POST['related_book']
        errors = Review.objects.review_validator(request.POST)

        if len(errors):
            for key,value in errors.items():
                messages.error(request,value)

            return redirect(loadbook,number=book_id)
        
        else:
            new_review = Review.objects.create(content=request.POST['book_review'],commentator=User.objects.get(id=request.session['user_id']),related_book=Book.objects.get(id=book_id),ratings=request.POST['ratings'])

            return redirect(loadbook,number=book_id)
