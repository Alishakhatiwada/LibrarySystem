from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from .forms import SignUpForm, BookForm
from .models import Book, BorrowHistory


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'catalog/book_list.html', {'books': books})


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available:
        BorrowHistory.objects.create(user=request.user, book=book)
        book.available = False
        book.save()
    return redirect('book_list')


@login_required
def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    borrow_record = BorrowHistory.objects.filter(user=request.user, book=book, returned_at__isnull=True).first()
    if borrow_record:
        borrow_record.returned_at = timezone.now()
        borrow_record.save()
        book.available = True
        book.save()
    return redirect('book_list')


@login_required
def history_view(request):
    history = BorrowHistory.objects.filter(user=request.user).order_by('-borrowed_at')
    return render(request, 'catalog/history.html', {'history': history})


@login_required
def user_dashboard(request):
    return render(request, 'catalog/user_dashboard.html')
