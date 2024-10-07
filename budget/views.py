from django.shortcuts import render,redirect
from django.views.generic import View
from budget.forms import ExpenseForm,RegisterForm,SignInForm
from django.contrib import messages
from budget.models import Expense
from django.db.models import Sum,Count
from django.contrib.auth.models import User
# Create your views here.

class ExpenseCreateView(View):
    def get(self,request,*args,**kwargs):
        form_instance=ExpenseForm()
        return render(request,'expensecreate.html',{'form':form_instance})
    def post(self,request,*args,**kwargs):
        form_instance=ExpenseForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            messages.success(request,'expense added')
            return redirect('expense-list')
        else:
             messages.error(request,'failed to add')
             return render(request,'expensecreate.html',{'form':form_instance})

class ExpenseListView(View):
    def get(self,request,*args,**kwargs):

        
        
        search_text=request.GET.get('search')
        selected_category=request.GET.get("category","all")
        if selected_category=='all':
            qs=Expense.objects.all()
        else:
            qs=Expense.objects.filter(category=selected_category)
        if search_text:
            qs=Expense.objects.filter(title__contains=search_text)
        
       
        return render(request,'expenselist.html',{'expenses':qs,"selected":selected_category})

class ExpenseUpdateView(View):
    def get(self,request,*args,**kwargs):

        # extract id from kwargs
        id=kwargs.get("pk")

        # fetch expense object with id
        expense_obj=Expense.objects.get(id=id)

        # initialize expense  with expense object
        form_instance=ExpenseForm(instance=expense_obj)

        return render(request,'expenseedit.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        expense_obj=Expense.objects.get(id=id)
        form_instance=ExpenseForm(request.POST,instance=expense_obj)
        if form_instance.is_valid():
            # data=form_instance.cleaned_data
            # Expense.objects.filter(id=id).update(**data)
            form_instance.save()
            messages.success(request,'updated!')
            return redirect('expense-list')
        
        else:
             messages.error(request,'failed to update')
             return render(request,'expenseedit.html',{'form':form_instance})

class ExpenseDeleteView(View):
    def get(self,request,*args,**kwargs):

        # extract id and delete expense with id
        Expense.objects.get(id=kwargs.get('pk')).delete()
        messages.success(request,'deleted successfully')
        return redirect('expense-list')
class ExpenseSummary(View):
    def get(self,request,*args,**kwargs):

        qs=Expense.objects.all()
        total_expenses=qs.count()
        total_amount=qs.values("amount").aggregate(amount_sum=Sum("amount"))
        category_summary=qs.values("category").annotate(category_count=Count("category"))
        amount_sum=qs.values("category").annotate(cat_sum=Sum("amount"))
        # print(total_amount)
       
        context={
            "total_expenses":total_expenses,
            "total_amount":total_amount,
            "category_count":category_summary,
            "category_amount_sum":amount_sum
            
        }
        return render(request,"expensesummary.html",context)

class SignUpView(View):
    template_name='register.html'
    def get(self,request,*args,**kwargs):
        form_instance=RegisterForm()
        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
        form_instance=RegisterForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            User.objects.create_user(**data)
            return redirect('signin')
        else:
            return render(request,self.template_name,{'form':form_instance})

class SignInView(View):
    template_name='login.html'
    def get(self,request,*args,**kwargs):
        form_instance=SignInForm()
        return render(request,self.template_name,{'form':form_instance})

    

