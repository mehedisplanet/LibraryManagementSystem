from django import forms
from .models import Book, UserReviews,BookPurchase

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserReviews
        fields = ['name','email','body']
        
    def __init__(self, *args, **kwargs):
        self.book = kwargs.pop('book', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        userBorrowed = BookPurchase.objects.filter(user=self.user, book=self.book).exists()
        if not userBorrowed:
            raise forms.ValidationError("You must borrow the book to make a review.")
        return cleaned_data