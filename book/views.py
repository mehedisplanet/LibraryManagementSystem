from typing import Any
from .import forms
from django.shortcuts import redirect
from .import models
from django.views.generic import DetailView
from .models import Book
from django.contrib import messages
from book.models import BookPurchase
from django.views import View
from .forms import ReviewForm
from transactions.views import send_transaction_email
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

class DetailsPostView(DetailView):
    model = models.Book
    template_name = 'book/bookDetails.html'
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()

        comment_form = ReviewForm(request.POST, book=post, user=request.user)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your review has been added successfully!')
            return self.get(request, *args, **kwargs)
        else:
            if not BookPurchase.objects.filter(user=request.user, book=post).exists():
                messages.error(request, 'Can not added your review')
            return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        reviews = post.comments.all()
        review_form= forms.ReviewForm()
            
        context['reviews']= reviews
        context['review_form']= review_form
        return context
    
@method_decorator(login_required, name='dispatch')
class PurchaseView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)

        if request.user.account.balance < book.price:
            messages.error(request, "Insufficient balance ")
        else:
            BookPurchase.objects.create(user=request.user, book=book,before_purchase_balance=request.user.account.balance, after_purchase_balance=request.user.account.balance - book.price )
            request.user.account.balance -= book.price
            request.user.account.save()

            messages.success(request, "Purchase successful.")
        send_transaction_email(self.request.user,book.price,"Purchase Message", 'transactions/purchaseEmail.html' )
        return redirect('profile')
    