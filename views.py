from django.shortcuts import render
from .models import UserModel,Income,Expense
# Create your views here.
from django.db.models import Sum
import json
from django.http import JsonResponse

def home(request):
    return render(request,"home.html")

def register(request,method=['GET','POST']):
    if request.method=='POST':
        username=request.POST.get("username")
        passw1=request.POST.get("password")
        passw2=request.POST.get("confirm_password")
        email=request.POST.get("email")
        q=UserModel.objects.filter(username=username)
           
        if(q):
            msg="User already exists"
            return render(request,"register.html",{"msg":msg})
        elif(passw1 != passw2):
            msg="Passwords does not match"
            return render(request,"register.html",{"msg":msg})
        else:
            UserModel.objects.create(username=username,password=passw1,email=email)
            q=UserModel.objects.get(username=username)
            return render(request,"login.html")
    return render(request,"register.html")

def login(request,method=['GET','POST']):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        q=UserModel.objects.filter(username=username,password=password)
        msg="User not found"
        if(q):            
            request.session["username"]=q[0].username
            return render(request,"main.html")
        else:
            return render(request,"login.html",{"msg":msg})
    return render(request,"login.html")

def main(request,method=['GET','POST']):
    if request.method=='POST':
        try:
            # Retrieve entry data from the request body
            data = json.loads(request.body)
            entry_type = data['type']
            name = data['name']
            date = data['date']
            amount = float(data['amount'])

            # Do something with the entry data, such as saving it to the database
            u=request.session['username']
            user=UserModel.objects.get(username=u)
            if str(entry_type)=="Expense":
                Expense.objects.create(user=user,name=name,date=date,amount=amount)
            elif(str(entry_type)=='Income'):
                Income.objects.create(user=user,name=name,date=date,amount=amount)

            # Return a success response
            response_data = {'message': 'Entry submitted successfully'}
            return JsonResponse(response_data)
        except Exception as e:
            # Return an error response if there's an exception
            return JsonResponse({'error': str(e)}, status=400)

    return render(request,"main.html")

def reports(request,method=['GET','POST']):
    total_income=0
    total_expense=0
    savings=0
    msg=""
    if request.method=='POST':
        month=request.POST.get("month")
        year=request.POST.get("year")
        u=request.session['username']
        user=UserModel.objects.get(username=u)
        expense_data = Expense.objects.filter(user=user,date__year=year, date__month=month)
        income_data = Income.objects.filter(user=user,date__year=year, date__month=month)
        try:

            # Calculate total income for the month
            print(expense_data)
            print(income_data)
            total_income = income_data.aggregate(total=Sum('amount'))['total']
            total_expense = expense_data.aggregate(total=Sum('amount'))['total']

            savings=int(total_income)-int(total_expense)
            return render(request,"reports.html",{"income":total_income,"expense":total_expense,"savings":savings})
        except:
            msg="no reports to generate"
            return render(request,"reports.html",{"income":total_income,"expense":total_expense,"savings":savings,"msg":msg})
    return render(request,"reports.html",{"income":total_income,"expense":total_expense,"savings":savings})
def logout(request):
    del request.session["username"]
    return render(request,"home.html")
   