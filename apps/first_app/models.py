from django.db import models
import re
from django.contrib import messages
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        #Checking for length
        if len(postData['first_name']) < 2:
            errors['first_name_len'] = "First name should have at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name_len'] = "Last name should have at least 2 characters"
        if len(postData['email']) < 2:
            errors['email_len'] = "Email should have at least 2 characters"
            #In the book reviewer, password has to be at least 8 characters long
        if len(postData['password']) < 8:
            errors['password_len'] = "Password should have at least 8 characters"
        #Making sure names are only letters
        if not postData['first_name'].isalpha():
            errors['first_name_alpha'] = "First name must contain only letters"
        if not postData['last_name'].isalpha():
            errors['last_name_alpha'] = "Last name must contain only letters"
        #Making sure email matches format
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Invalid email format"
        #Making sure email isn't already in the list
        if User.objects.filter(email=postData['email']):
            errors['already_registered'] = "Email is already in the database"
        #Making sure both passwords match
        if postData['password'] != postData['confirm_password']:
            errors['password_match'] = "Both passwords need to  match"
        return errors
    
    def login_validator(self,postData):
        errors = {}
        #Checking length
        if len(postData['email']) < 2:
            errors['email_len_login'] = "Email should have at least 2 characters"
        if len(postData['password']) < 2:
            errors['password_len_login'] = "Password should have at least 2 characters"
        #Checking email format
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format_login'] = "Invalid email format"
        #Checking if email is in the database
        if not User.objects.filter(email=postData['email']):
            errors['email_db_check'] = "Invalid credentials"
        else:
            log_user = User.objects.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), log_user.password.encode()):
                errors['pw_db_check'] = "Invalid credentials"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class BookManager(models.Manager):
    def book_validator(self,postData):
        errors = {}
        #Checking for length in book title and book author
        if len(postData['new_title']) < 2:
            errors['book_title_len'] = "Book Title should have at least 2 characters"
        if postData['regular_author'] == "add":
            if len(postData['new_author']) < 2:
                errors['book_author_len'] = "Book author name should have at least 2 characters"
        if len(postData['book_review']) < 10:
            errors['review_len'] = "Review shouldhave at least 10 characters"
        return errors


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="authored_books")
    uploader = models.ForeignKey(User, related_name="user_list_of_uploaded_books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()

class ReviewManager(models.Manager):
    def review_validator(self,postData):
        errors = {}
        if len(postData['book_review']) < 2:
            errors['book_review_len'] = "Book Review should have at least 2 characters"
        return errors

class Review(models.Model):
    content = models.TextField()
    commentator = models.ForeignKey(User, related_name="user_list_of_reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    related_book = models.ForeignKey(Book, related_name="reviews_for_book")
    ratings = models.IntegerField()
    objects = ReviewManager()