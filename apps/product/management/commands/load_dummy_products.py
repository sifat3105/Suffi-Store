import requests
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from apps.product.models import Category, Product, ProductImage, Tag, ProductTag

API_URL = "https://dummyjson.com/products"


class Command(BaseCommand):
    help = "Load dummy products from dummyjson.com into the database"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Fetching data from DummyJSON..."))
        response = requests.get(API_URL)
        data = response.json()

        products = data.get("products", [])
        self.stdout.write(self.style.NOTICE(f"Found {len(products)} products"))

        for item in products:
            # 🏷️ Category
            category_name = item.get("category", "Uncategorized")
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={"slug": slugify(category_name)},
            )

            # 🛒 Product
            old_price = None
            if item.get("discountPercentage"):
                old_price = round(
                    item["price"] + (item["price"] * (item["discountPercentage"] / 100)), 2
                )

            product, created = Product.objects.get_or_create(
                title=item["title"],
                defaults={
                    "description": item.get("description", ""),
                    "price": item["price"],
                    "old_price": old_price,
                    "rating": item.get("rating", 0),
                    "brand": item.get("brand", ""),
                    "category": category,
                    "slug": slugify(item["title"]),
                    "stock_status": "in-stock" if item.get("stock", 0) > 0 else "out-of-stock",
                    "is_active": True,
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added product: {product.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipped existing product: {product.title}"))

            # 🏷️ Tags
            tags = item.get("tags", [])
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={"slug": slugify(tag_name)}
                )
                ProductTag.objects.get_or_create(product=product, tag=tag)

            # 🖼️ Images
            for idx, img_url in enumerate(item.get("images", [])):
                ProductImage.objects.get_or_create(
                    product=product,
                    image=img_url,
                    defaults={
                        "alt_text": f"{product.title} image {idx + 1}",
                        "is_primary": idx == 0,
                        "order": idx,
                    }
                )

        self.stdout.write(self.style.SUCCESS("✅ Dummy products loaded successfully!"))
