from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validador_campos(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        JUST_LETTERS = re.compile(r'^[a-zA-Z.]+$')
        PASSWORD_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')

        errors = {}

        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email_exits'] = "Email ya registrado!!!"
        else:
            if len(postData['first_name'].strip()) < 2 or len(postData['first_name'].strip()) > 50:
                errors['first_name_len'] = "Nombre debe tener entre 2 y 50 caracteres"

            if len(postData['last_name'].strip()) < 2 or len(postData['last_name'].strip()) > 50:
                errors['last_name_len'] = "Apellido debe tener entre 2 y 50 caracteres"
            
            if not JUST_LETTERS.match(postData['first_name']) or not JUST_LETTERS.match(postData['last_name']):
                errors['just_letters'] = "Solo se permite el ingreso de letras en el nombre y apellido"
                
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Formato correo no válido"
            
            if not PASSWORD_REGEX.match(postData['password']):
                errors['password_format'] = "Formato contraseña no válido"

        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Contraseñas no coinciden"

        return errors

class JobManager(models.Manager):
    def validador_campos(self, postData):
        errors = {}
        if len(postData['title'].strip()) < 3:
            errors['title_len'] = "El título del trabajo debe tener al menos 4 caracteres"
        if len(postData['description'].strip()) < 10:
            errors['description_len'] = "La descripción debe tener al menos 10 caracteres"
        if len(postData['location'].strip()) < 1:
            errors['location_len'] = "La dirección no puede estar vacia"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Job(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    location = models.CharField(max_length=100)
    creater = models.ForeignKey(User, related_name="user_creater", on_delete = models.CASCADE)
    worker = models.ForeignKey(User, related_name="user_worker", blank=True, null=True, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

    def __str__(self):
        return self.title
    