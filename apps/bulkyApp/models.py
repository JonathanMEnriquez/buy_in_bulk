# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
import datetime
from time import strftime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")

class UserManager(models.Manager):
    def ageValidator(self, postData):
        try:
            dob = postData['dob']
            date_of_birth = dob.replace("-","")
            year = datetime.datetime.now().year
            dob = int(date_of_birth) / 10000
            if (year - dob) < 12 or (year - dob) > 123:
                return False
        except:
            return False
        return True

    def validateRegistration(self, postData):
        response = {}
        if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['username']) < 1 or len(postData['password']) < 1:
            try:
                response['error'].append("Please fill in all fields")
            except:
                response['error'] = []
                response['error'].append("Please fill in all fields")
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha() or len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            try:
                response['error'].append("Please enter a valid name")
            except:
                response['error'] = []
                response['error'].append("Please enter a valid name")
        if not User.objects.ageValidator(postData):
            try:
                response['error'].append("Please enter a valid date of birth")
            except:
                response['error'] = []
                response['error'].append("Please enter a valid date of birth")
        if not EMAIL_REGEX.match(postData['email']):
            try:
                response['error'].append("Please enter a valid email address")
            except:
                response['error'] = []
                response['error'].append("Please enter a valid email address")
        if postData['password'] != postData['confirm_password']:
            try:
                response['error'].append("Password and Confirm Password must match")
            except:
                response['error'] = []
                response['error'].append("Password and Confirm Password must match")
        if not PASS_REGEX.match(postData['password']):
            try:
                response['error'].append("Passwords must be at least 8 characters, including 1 lowercase, 1 uppercase, 1 special character, and 1 number")
            except:
                response['error'] = []
                response['error'].append("Passwords must be at least 8 characters, including 1 lowercase 1 uppercase, 1 special character, and 1 number")
        db_email_check = User.objects.filter(email = postData['email'])
        if len(db_email_check) > 0:
            try:
                response['error'].append("Email is already registered")
            except:
                response['error'] = []
                response['error'].append("Email is already registered")
        db_username_check = User.objects.filter(username = postData['username'])
        if len(db_username_check) > 0:
            try:
                response['error'].append("Username is already taken")
            except:
                response['error'] = []
                response['error'].append("Username is already taken")
        return response
    
    def addUser(self, postData):
        password = postData['password']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        newuser = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], username = postData['username'], date = postData['dob'], password = hashed_pw)
        return newuser

    def validateLogin(self, postData):
        check_login_em = User.objects.filter(email = postData['email'])
        if len(check_login_em) > 0:
            retrieved_pass = User.objects.get(email = postData['user_input']).password
        if not bcrypt.checkpw(input_password.encode(), retrieved_pass.encode()):
            return False
        else:
            user_id = User.objects.get(email = postData['user_input']).id
            return user_id

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    address = models.ForeignKey(Postal_Address, related_name="belongs_to")
    date = models.DateField(max_length = 8, null=True)
    password = models.CharField(max_length = 355)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return "User Full Name: {} {}, Email: {}, Password: {}".format(self.first_name, self.last_name, self.email, self.password)

class Supplier(models.Model):
    company_name = models.CharField(max_length = 300)

class Item(models.Model):
    make = models.CharField(max_length = 100)
    model = models.CharField(max_length = 150)
    model_more_info = models.CharField(max_length = 150, blank = True)
    supplier = models.ForeignKey(Supplier, related_name = "items")
    color = models.CharField(max_length = 30, blank = True)

class Distribution_Center(models.Model):
    owned_by = models.ForeignKey(Supplier, related_name="distribution_centers")
    
class Postal_Address(models.Model):
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(_(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zip_code = models.Charfield(max_length=5)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return "{}, {}, \n{}, {}, {}".format(self.address_1, self.address_2, self.city, self.state, self.zip_code)