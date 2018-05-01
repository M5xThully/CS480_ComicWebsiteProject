from django.http import HttpResponse
from django.shortcuts import render

def home(request):
	return render(request,'frontpage.html')

def login(request):
	return render(request,'loginpage.html')

def register(request):
	return render(request,'registerpage.html')
	
