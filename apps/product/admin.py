from django.contrib import admin
from django.utils.html import format_html
from django import forms
from unfold.admin import ModelAdmin
from unfold.decorators import display
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, ProductImage, Tag, ProductTag
from django.urls import reverse



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    max_num = 10
    fields = ('image', 'alt_text', 'is_primary', 'order')
    verbose_name = 'Product Image'
    verbose_name_plural = 'Product Images'


class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 1
    verbose_name = 'Product Tag'
    verbose_name_plural = 'Product Tags'
    autocomplete_fields = ['tag']


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'rating': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'max': '5',
                'placeholder': '0.0 - 5.0',
                'style': 'width: 200px;'
            }),
            'stock_status': forms.Select(attrs={
                'class': 'vSelectField',
                'style': 'width: 200px;'
            }),
        }


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    form = ProductAdminForm
    inlines = [ProductImageInline, ProductTagInline]
    
    list_display = [
        'id',
        'title_display',
        'category_display',
        'quantity',
        'price_display', 
        'old_price_display',
        'discount_percentage_badge',
        'stock_status_badge',
        'rating_stars',
        'is_active_toggle',
        'created_at_formatted',
    ]
    
    list_filter = [
        'stock_status', 
        'is_active', 
        'category',
        'created_at', 
        'rating'
    ]
    
    search_fields = ['title', 'description', 'badge']
    search_help_text = 'Search by title, description, or badge'
    
    readonly_fields = [
        'discount_percentage_display', 
        'created_at', 
        'updated_at',
        'preview_images'
    ]
    
    fieldsets = [
        (_('📋 Basic Information'), {
            'fields': [
                'title', 
                'category',
                'description', 
                'about_product',
            ],
            'classes': ['basic-information']
        }),
        (_('💰 Pricing Information'), {
            'fields': [
                'old_price', 
                'price', 
                'unit',
                'discount_percentage_display'
            ],
            'classes': ['pricing-information']
        }),
        (_('🏷️ Product Details'), {
            'fields': [
                'badge',
                'rating',
                'quantity',
                'stock_status', 
                'is_active'
            ],
            'classes': ['product-details']
        }),
        (_('🖼️ Image Preview'), {
            'fields': ['preview_images'],
            'classes': ['image-preview']
        }),
        (_('⏰ Timestamps'), {
            'fields': [
                'created_at', 
                'updated_at'
            ],
            'classes': ['collapse', 'timestamps']
        })
    ]
    
    filter_horizontal = []
    list_per_page = 25
    save_on_top = True
    
    # Define actions as a list (not a method)
    actions = ['make_active', 'make_inactive', 'clear_discounts']

    @admin.action(description="Clear category from selected products")
    def clear_category(self, request, queryset):
        updated = queryset.update(category=None)
        self.message_user(request, f"Cleared category from {updated} products.")
        return None

    # include the new action in the actions list
    actions = actions + ['clear_category']
    
    @admin.action(description="Mark selected products as active")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} products were marked as active.")
    
    @admin.action(description="Mark selected products as inactive")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} products were marked as inactive.")
    
    @admin.action(description="Clear discounts from selected products")
    def clear_discounts(self, request, queryset):
        updated = queryset.update(old_price=None)
        self.message_user(request, f"Discounts cleared from {updated} products.")
    
    @display(description=_('Title'), ordering='title')
    def title_display(self, obj):
        return format_html(
            '<strong>{}</strong><br><small style="color: #6b7280;">{}</small>',
            obj.title,
            obj.badge if obj.badge else 'No badge'
        )
    
    @display(description=_('Category'), ordering='category__name')
    def category_display(self, obj):
        if obj.category:
            # build admin change url for the Category instance dynamically
            try:
                url = reverse(
                    'admin:%s_%s_change' % (obj.category._meta.app_label, obj.category._meta.model_name),
                    args=(obj.category.pk,)
                )
                return format_html(
                    '<a href="{}" style="font-weight: 500; color: #2563eb; text-decoration: none;">{}</a>',
                    url,
                    obj.category.name
                )
            except Exception:
                # fallback to plain text if reverse fails for any reason
                return format_html('<span style="font-weight: 500; color: #2563eb;">{}</span>', obj.category.name)
        return format_html('<span style="color: #9ca3af;">Uncategorized</span>')
    
    @display(description=_('Price'), ordering='price')
    def price_display(self, obj):
        return format_html(
            '<span style="font-family: monospace; color: #059669;">${}</span>',
            obj.price
        )
    
    @display(description=_('Old Price'), ordering='old_price')
    def old_price_display(self, obj):
        if obj.old_price:
            return format_html(
                '<span style="font-family: monospace; color: #dc2626; text-decoration: line-through;">${}</span>',
                obj.old_price
            )
        return format_html('<span style="color: #9ca3af;">—</span>')
    
    @display(description=_('Discount'), ordering='discount_percentage')
    def discount_percentage_badge(self, obj):
        discount = obj.discount_percentage
        if discount > 0:
            return format_html(
                '<span style="padding: 0.25rem 0.5rem; font-size: 0.75rem; font-weight: bold; border-radius: 9999px; background-color: #dcfce7; color: #166534;">{}% OFF</span>',
                discount
            )
        return format_html('<span style="color: #9ca3af;">—</span>')
    
    @display(description=_('Stock Status'), ordering='stock_status')
    def stock_status_badge(self, obj):
        status_colors = {
            'in-stock': 'background-color: #dcfce7; color: #166534;',
            'out-of-stock': 'background-color: #fee2e2; color: #dc2626;',
            'low-stock': 'background-color: #fef3c7; color: #d97706;',
            'discontinued': 'background-color: #f3f4f6; color: #374151;',
        }
        color_style = status_colors.get(obj.stock_status, 'background-color: #f3f4f6; color: #374151;')
        return format_html(
            '<span style="padding: 0.25rem 0.5rem; font-size: 0.75rem; font-weight: 500; border-radius: 9999px; {}">{}</span>',
            color_style,
            obj.get_stock_status_display()
        )
    
    @display(description=_('Rating'), ordering='rating')
    def rating_stars(self, obj):
        stars = '★' * int(obj.rating) + '☆' * (5 - int(obj.rating))
        return format_html(
            '<span style="font-family: monospace; color: #d97706;">{}</span> <small style="color: #6b7280;">({})</small>',
            stars,
            obj.rating
        )
    
    @display(description=_('Active'))
    def is_active_toggle(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="padding: 0.25rem 0.5rem; font-size: 0.75rem; font-weight: bold; border-radius: 9999px; background-color: #dcfce7; color: #166534;">✓ Active</span>'
            )
        return format_html(
            '<span style="padding: 0.25rem 0.5rem; font-size: 0.75rem; font-weight: bold; border-radius: 9999px; background-color: #fee2e2; color: #dc2626;">✗ Inactive</span>'
        )
    
    @display(description=_('Created'))
    def created_at_formatted(self, obj):
        return format_html(
            '<span style="font-size: 0.875rem; color: #6b7280;">{}</span>',
            obj.created_at.strftime('%Y-%m-%d %H:%M')
        )
    
    def discount_percentage_display(self, obj):
        if obj.discount_percentage > 0:
            return format_html(
                '<div style="padding: 0.75rem; background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 0.5rem;">'
                '<span style="font-size: 1.5rem; font-weight: bold; color: #059669;">{}%</span>'
                '<br><span style="font-size: 0.875rem; color: #059669;">Discount</span>'
                '</div>',
                obj.discount_percentage
            )
        return format_html(
            '<div style="padding: 0.75rem; background-color: #f9fafb; border: 1px solid #d1d5db; border-radius: 0.5rem; color: #6b7280;">No discount</div>'
        )
    discount_percentage_display.short_description = _('Discount Percentage')
    
    def preview_images(self, obj):
        if obj.pk:
            images = obj.images.all()[:4]
            if images:
                image_html = ''.join([
                    f'<div style="display: inline-block; margin: 0.25rem;"><img src="{img.image.url}" alt="{img.alt_text}" style="width: 4rem; height: 4rem; object-fit: cover; border-radius: 0.25rem; border: 1px solid #d1d5db;" title="{img.alt_text}"></div>'
                    for img in images
                ])
                return format_html(
                    '<div style="display: flex; flex-wrap: wrap;">{}</div>'
                    '<div style="margin-top: 0.5rem; font-size: 0.875rem; color: #6b7280;">Total images: {}</div>',
                    image_html, obj.images.count()
                )
        return format_html('<span style="color: #9ca3af;">Save product to see images</span>')
    preview_images.short_description = _('Image Gallery Preview')
    
    def get_queryset(self, request):
        # include related category to ensure ordering and display work without extra queries
        return super().get_queryset(request).select_related('category').prefetch_related('images', 'product_tags__tag')


@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    list_display = [
        'image_preview',
        'product_link',
        'alt_text_display',
        'is_primary_badge',
        'order',
    ]
    
    list_filter = ['is_primary', 'product']
    search_fields = ['product__title', 'alt_text']
    list_editable = ['order']
    list_per_page = 20
    
    # Define actions as a list
    actions = ['make_primary', 'delete_selected']
    
    @admin.action(description="Mark selected images as primary")
    def make_primary(self, request, queryset):
        # First, set all images of these products to non-primary
        product_ids = queryset.values_list('product_id', flat=True).distinct()
        ProductImage.objects.filter(product_id__in=product_ids).update(is_primary=False)
        
        # Then set the selected ones as primary
        updated = queryset.update(is_primary=True)
        self.message_user(request, f"{updated} images were marked as primary.")
    
    @display(description=_('Image'))
    def image_preview(self, obj):
        # Safely render image preview. Some environments may not serve MEDIA files
        # (or image.url access may raise), so guard and fall back to a small
        # placeholder box.
        url = None
        try:
            if obj.image:
                url = obj.image.url
        except Exception:
            url = None

        if url:
            return format_html(
                '<img src="{}" alt="{}" style="width: 3rem; height: 3rem; object-fit: cover; border-radius: 0.25rem; border: 1px solid #d1d5db;" loading="lazy" onerror="this.style.opacity=.5">',
                url, obj.alt_text or 'Product image'
            )

        # Inline placeholder (avoids relying on a static file path)
        return format_html(
            '<div style="width: 3rem; height: 3rem; display:flex; align-items:center; justify-content:center; background:#f3f4f6; border-radius:0.25rem; border:1px solid #d1d5db; color:#9ca3af; font-size:0.75rem;">{}</div>',
            'No image'
        )
    
    @display(description=_('Product'), ordering='product__title')
    def product_link(self, obj):
        return format_html(
            '<a href="/admin/products/product/{}/change/" style="font-weight: 500; color: #2563eb; text-decoration: none;">{}</a>',
            obj.product.id, obj.product.title
        )
    
    @display(description=_('Alt Text'))
    def alt_text_display(self, obj):
        return obj.alt_text or format_html('<span style="color: #9ca3af;">—</span>')
    
    @display(description=_('Primary'))
    def is_primary_badge(self, obj):
        if obj.is_primary:
            return format_html(
                '<span style="padding: 0.25rem 0.5rem; font-size: 0.75rem; font-weight: bold; border-radius: 9999px; background-color: #dbeafe; color: #1e40af;">Primary</span>'
            )
        return format_html('<span style="color: #9ca3af;">—</span>')


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}
    list_per_page = 20
    
    # Define actions as a list
    actions = ['merge_tags']
    
    @admin.action(description="Merge selected tags into first tag")
    def merge_tags(self, request, queryset):
        if queryset.count() < 2:
            self.message_user(request, "Please select at least 2 tags to merge.", level='error')
            return
        
        primary_tag = queryset.first()
        other_tags = queryset.exclude(id=primary_tag.id)
        
        # Update all product tags to use the primary tag
        for tag in other_tags:
            ProductTag.objects.filter(tag=tag).update(tag=primary_tag)
        
        # Delete the merged tags
        deleted_count = other_tags.count()
        other_tags.delete()
        
        self.message_user(request, f"Merged {deleted_count} tags into '{primary_tag.name}'.")
    
    @display(description=_('Products'), ordering='product_count')
    def product_count(self, obj):
        count = ProductTag.objects.filter(tag=obj).count()
        return format_html(
            '<span style="padding: 0.25rem 0.5rem; font-size: 0.75rem; font-weight: 500; border-radius: 9999px; background-color: #f3f4f6;">{}</span>',
            count
        )
    


from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import WeeklySpecialProduct

@admin.register(WeeklySpecialProduct)
class WeeklySpecialProductAdmin(ModelAdmin):
    list_display = ("product", "start_date", "end_date")
    list_filter = ("start_date", "end_date")
    search_fields = ("product__title",)
    ordering = ("-start_date",)

    fieldsets = (
        ("Product Info", {"fields": ("product",)}),
        ("Duration", {"fields": ("start_date", "end_date")}),
    )

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}

