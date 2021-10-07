from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def home(request): #ir al home
    return render(request, ('handy_app/home.html'))

def register(request): #registrar un usuario
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        errors = User.objects.validador_campos(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            #Si se produce un error pero no queremos perder los datos....
            request.session['level_mensaje'] = 'alert-danger'
            return redirect('/') 
        else:
            request.session['registro_nombre'] = ""
            request.session['registro_apellido'] = ""
            request.session['registro_email'] = ""
           
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

            obj = User.objects.create(first_name=first_name, last_name=last_name,email=email,password=password_hash)
            obj.save()
            messages.success(request, "Usuario registrado con éxito!!!!")
            request.session['level_mensaje'] = 'alert-success'
            
        return redirect('/')

    return render(request, 'handy_app/login.html')

def login(request):
    if request.method == 'GET':
        return redirect("/")
    else:
        if request.method == 'POST':
            user = User.objects.filter(email=request.POST['email_login'])
            #Buscamos el correo ingresado en la BD             
            if user : #Si el usuario existe
                usuario_registrado = user[0]
                if bcrypt.checkpw(request.POST['password_login'].encode(), usuario_registrado.password.encode()):
                    usuario = { # session
                        'id':usuario_registrado.id,
                        'first_name':usuario_registrado.first_name,
                        'last_name':usuario_registrado.last_name,
                        'email':usuario_registrado.email,
                        # 'rol':usuario_registrado.rol,
                    }

                    request.session['usuario'] = usuario
                    
                    return redirect('/dashboard')
                else:
                    messages.error(request,"Datos mal ingresados o el usuario no existe!!!")
                    return redirect('/')
            else:
                messages.error(request,"Datos mal ingresados o el usuario no existe!!!")
                return redirect('/')

def dashboard(request):
    context = {
        'jobs': Job.objects.all().order_by('-created_at').order_by('-updated_at'),
    }
    return render(request, 'handy_app/dashboard.html', context)

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
        return redirect('/')   

def addjob(request):
    if 'usuario' in request.session:
        return render(request, 'handy_app/create_job.html')
    else:
        return redirect('/')

def create_job(request):
    if request.method == 'GET':
        return redirect("/addjob")
    else:
        if request.method == 'POST':
            errors = Job.objects.validador_campos(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            #Si se produce un error pero no queremos perder los datos....
            request.session['level_mensaje'] = 'alert-danger'
            return redirect('/addjob') 
        else:
            nombrecito = request.POST['title']
            quehago = request.POST['description']
            direccion = request.POST['location']
            creador_job = User.objects.get(id=request.session['usuario']['id'])

            obj_job = Job.objects.create(title=nombrecito, description=quehago, location=direccion, creater=creador_job)
            obj_job.save()
        return redirect('/dashboard')


def view_job(request, job_id):
    context = {
        'tarea': Job.objects.get(id=job_id),
    }
    return render(request,'handy_app/view_job.html', context)

def erase_job(request, job_id):
    #if "user_data" not in request.session:
        #return redirect("/")
    borrar_tarea = Job.objects.get(id=job_id)
    borrar_tarea.delete()
    return redirect('/dashboard')

def assign(request, job_id):
        tarea_assign = Job.objects.get(id=job_id)
        tarea_assign.worker=User.objects.get(id=request.session['usuario']['id'])
        tarea_assign.save()
        return redirect('/dashboard')


def edit(request, job_id):
    context = {
        'edit_tarea': Job.objects.get(id=job_id),
    }
    return render(request,'handy_app/edit_job.html', context)

