"""
Example usage of Django Admin Query Executor

This file demonstrates how to integrate the django-admin-query-executor
package into your Django admin.
"""

from django.contrib import admin
from django.db.models import Count, Q, Avg, Sum
from django_admin_query_executor import QueryExecutorMixin

# Import your models
from myapp.models import Book, Author, Publisher, Review


@admin.register(Book)
class BookAdmin(QueryExecutorMixin, admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'price', 'published_date']
    list_filter = ['published_date', 'publisher', 'category']
    search_fields = ['title', 'author__name', 'isbn']

    # Define custom query examples for your model
    query_examples = [
        # (Description, Query)
        ("All books", "Book.objects.all()"),
        ("Recent books (last 30 days)", "Book.objects.filter(published_date__gte=timezone.now() - timedelta(days=30))"),
        ("Bestsellers", "Book.objects.filter(is_bestseller=True)"),
        ("By price range ($20-$50)", "Book.objects.filter(price__gte=20, price__lte=50)"),
        ("Fiction or Non-fiction", "Book.objects.filter(Q(category='Fiction') | Q(category='Non-fiction'))"),
        ("Books with reviews", "Book.objects.annotate(review_count=Count('reviews')).filter(review_count__gt=0)"),
        ("Average price by category", "Book.objects.values('category').annotate(avg_price=Avg('price'))"),
        ("Top rated books", "Book.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=4.0).order_by('-avg_rating')[:10]"),
        ("Books by specific author", "Book.objects.filter(author__name__icontains='Smith')"),
        ("Count by publisher", "Book.objects.values('publisher__name').annotate(count=Count('id')).order_by('-count')"),
    ]

    # Optional: Customize the number of queries shown in history
    query_history_limit = 10  # Default is 5


@admin.register(Author)
class AuthorAdmin(QueryExecutorMixin, admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'nationality', 'book_count']
    list_filter = ['nationality', 'birth_date']
    search_fields = ['name', 'biography']

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Number of Books'

    query_examples = [
        ("All authors", "Author.objects.all()"),
        ("Authors with books", "Author.objects.filter(books__isnull=False).distinct()"),
        ("Prolific authors (5+ books)", "Author.objects.annotate(book_count=Count('books')).filter(book_count__gte=5)"),
        ("Authors by nationality", "Author.objects.filter(nationality='American')"),
        ("Authors born after 1950", "Author.objects.filter(birth_date__year__gte=1950)"),
        ("Total books by author", "Author.objects.annotate(total_books=Count('books')).order_by('-total_books')[:20]"),
        ("Authors with bestsellers", "Author.objects.filter(books__is_bestseller=True).distinct()"),
    ]


@admin.register(Publisher)
class PublisherAdmin(QueryExecutorMixin, admin.ModelAdmin):
    list_display = ['name', 'founded', 'country', 'active']
    list_filter = ['active', 'country']
    search_fields = ['name', 'description']

    query_examples = [
        ("Active publishers", "Publisher.objects.filter(active=True)"),
        ("Publishers by country", "Publisher.objects.filter(country='USA')"),
        ("Publishers with many books", "Publisher.objects.annotate(book_count=Count('book')).filter(book_count__gt=10)"),
        ("Revenue by publisher", "Publisher.objects.annotate(total_revenue=Sum('book__price')).order_by('-total_revenue')"),
        ("Recent publishers", "Publisher.objects.filter(founded__gte=2000)"),
    ]


@admin.register(Review)
class ReviewAdmin(QueryExecutorMixin, admin.ModelAdmin):
    list_display = ['book', 'reviewer_name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'reviewer_name', 'comment']

    query_examples = [
        ("Recent reviews", "Review.objects.filter(created_at__gte=timezone.now() - timedelta(days=7))"),
        ("5-star reviews", "Review.objects.filter(rating=5)"),
        ("Reviews with comments", "Review.objects.exclude(comment='')"),
        ("Average rating by book", "Review.objects.values('book__title').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')"),
        ("Review count by rating", "Review.objects.values('rating').annotate(count=Count('id')).order_by('rating')"),
    ]


# Example with existing admin class - just add the mixin
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'total', 'status', 'created_at']
    # ... existing admin configuration ...

# Add QueryExecutorMixin to enable query functionality
class OrderAdminWithQuery(QueryExecutorMixin, OrderAdmin):
    query_examples = [
        ("Pending orders", "Order.objects.filter(status='pending')"),
        ("High value orders", "Order.objects.filter(total__gte=100)"),
        ("Orders by status", "Order.objects.values('status').annotate(count=Count('id'))"),
    ]

# Re-register with the new admin class
admin.site.unregister(Order)
admin.site.register(Order, OrderAdminWithQuery)


# Advanced example with custom configuration
@admin.register(Product)
class ProductAdmin(QueryExecutorMixin, admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'sku']

    # Extensive query examples showing various ORM features
    query_examples = [
        # Basic queries
        ("All products", "Product.objects.all()"),
        ("Active products", "Product.objects.filter(is_active=True)"),
        ("Out of stock", "Product.objects.filter(stock=0)"),

        # Complex filters
        ("Low stock (< 10)", "Product.objects.filter(stock__lt=10, stock__gt=0)"),
        ("Price range $10-$50", "Product.objects.filter(price__range=(10, 50))"),
        ("Name contains 'Pro'", "Product.objects.filter(name__icontains='pro')"),

        # Using Q objects
        ("Electronic OR Books", "Product.objects.filter(Q(category='Electronics') | Q(category='Books'))"),
        ("Expensive OR Low stock", "Product.objects.filter(Q(price__gt=100) | Q(stock__lt=5))"),

        # Annotations
        ("With order count", "Product.objects.annotate(order_count=Count('orderitem')).filter(order_count__gt=0)"),
        ("Revenue per product", "Product.objects.annotate(revenue=Sum('orderitem__quantity') * F('price')).order_by('-revenue')[:10]"),

        # Aggregations
        ("Average price", "Product.objects.aggregate(avg_price=Avg('price'), total_products=Count('id'))"),
        ("Stock summary", "Product.objects.aggregate(total_stock=Sum('stock'), avg_stock=Avg('stock'))"),

        # Complex queries
        ("Best sellers", "Product.objects.annotate(sold=Sum('orderitem__quantity')).filter(sold__gt=0).order_by('-sold')[:20]"),
        ("Category statistics", "Product.objects.values('category').annotate(count=Count('id'), avg_price=Avg('price'), total_stock=Sum('stock'))"),

        # Date queries
        ("Created this month", "Product.objects.filter(created_at__month=timezone.now().month, created_at__year=timezone.now().year)"),
        ("Modified recently", "Product.objects.filter(updated_at__gte=timezone.now() - timedelta(days=7))"),

        # Related queries
        ("With reviews", "Product.objects.filter(reviews__isnull=False).distinct()"),
        ("Highly rated", "Product.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=4.5)"),
    ]

    # Increase history limit for this admin
    query_history_limit = 15


# Minimal example - the mixin provides default query examples
@admin.register(Tag)
class TagAdmin(QueryExecutorMixin, admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    # No query_examples defined - will use defaults:
    # - Model.objects.all()
    # - Model.objects.filter(id=1)
    # - Model.objects.count()


# Dark Mode Customization Example
# You can customize the dark mode colors by adding CSS to your project

# Option 1: Add to your admin/base_site.html template
"""
{% extends "admin/base_site.html" %}
{% block extrastyle %}
{{ block.super }}
<style>
/* Customize Query Executor dark mode colors */
.query-executor-container {
    /* Primary backgrounds */
    --qe-bg-primary: #0d1117;  /* GitHub dark style */
    --qe-bg-secondary: #161b22;
    --qe-bg-tertiary: #21262d;

    /* Text colors */
    --qe-text-primary: #c9d1d9;
    --qe-text-secondary: #8b949e;

    /* Accent colors */
    --qe-button-primary-bg: #238636;
    --qe-button-primary-hover: #2ea043;

    /* Borders */
    --qe-border-color: #30363d;
    --qe-border-hover: #58a6ff;
}

/* Apply same colors to dark mode */
body.theme-dark .query-executor-container,
.dark-mode .query-executor-container {
    --qe-bg-primary: #0d1117;
    --qe-bg-secondary: #161b22;
    --qe-bg-tertiary: #21262d;
}
</style>
{% endblock %}
"""

# Option 2: Add a custom CSS file
# Create static/admin/css/custom_admin.css and include it in your admin
class CustomStyledAdmin(QueryExecutorMixin, admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
