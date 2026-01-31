
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


UNFOLD = {
    "SITE_TITLE": "Sufi's Admin Dashboard",
    "SITE_HEADER": "Sufi's Admin Dashboard",
    "SITE_SUBHEADER": "Manage Your Data",
    "SITE_ICON": lambda request: static("admin/sufis.svg"),
    "SITE_ICON": {
        "light": lambda request: static("admin/sufis.svg"),
        "dark": lambda request: static("admin/sufis.svg"),
    },
    "STYLES": [
        lambda request: static("css/admin_custom.css"),
        lambda request: static("css/admin_dashboard.css"),
    ],
    "SHOW_HISTORY": True,
    "SHOW_EDIT_BUTTON": True,
    "SHOW_VIEW_ON_SITE_BUTTON": True,
    "DASHBOARD_CALLBACK": "project.views.dashboard_callback",
    "THEME": "light",  # Force light theme and disable theme switcher
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": "Dashboard",
                "separator": False,
                "collapsible": False,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "User Management",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group
                "items": [
                    {
                        "title": "Users",
                        "icon": "people",
                        "link": reverse_lazy("admin:user_user_changelist"),
                    },
                    {
                        "title": "Profiles",
                        "icon": "person",
                        "link": reverse_lazy("admin:user_account_changelist"),
                    },
                ],
            },
            {
                "title": "Products",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Products List",
                        "icon": "package_2",
                        "link": reverse_lazy("admin:product_product_changelist"),
                    },
                    {
                        "title": "Product Category",
                        "icon": "category",
                        "link": reverse_lazy("admin:product_category_changelist"),
                    },
                    {
                        "title": "Weekly Special Products",
                        "icon": "image",
                        "link": reverse_lazy("admin:product_weeklyspecialproduct_changelist"),
                    },
                ],
            },
            {
                "title": "Carts & Orders",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Users Cart's List",
                        "icon": "add_shopping_cart",
                        "link": reverse_lazy("admin:cart_cart_changelist"),
                    },
                    {
                        "title": "Users Cart Items",
                        "icon": "box_add",
                        "link": reverse_lazy("admin:cart_cartitem_changelist"),
                    },
                    {
                        "title": "Discount Coupons",
                        "icon": "local_activity",
                        "link": reverse_lazy("admin:cart_couponcode_changelist"),
                    },
                    {
                        "title": "User Orders",
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:order_order_changelist"),
                    },
                ],
            },
            {
                "title": "Delivery Options & Addresses",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Postal Codes",
                        "icon": "location_on",
                        "link": reverse_lazy("admin:address_postalcode_changelist"),
                    },
                    {
                        "title": "Shipping Charges",
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:address_shippingcharge_changelist"),
                    },
                ],
            },
            {
                "title": "Reviews & Contacts",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Reviews List",
                        "icon": "reviews",
                        "link": reverse_lazy("admin:review_review_changelist"),
                    },
                    {
                        "title": "Contact Us Messages",
                        "icon": "contact_emergency",
                        "link": reverse_lazy("admin:review_contactus_changelist"),
                    },
                    # {
                    #     "title": "Weekly Special Products",
                    #     "icon": "image",
                    #     "link": reverse_lazy("admin:product_weeklyspecialproduct_changelist"),
                    # },
                ],
            },
            # {
            #     "title": "Parts",
            #     "separator": True,
            #     "collapsible": False,
            #     "items": [
            #         {
            #             "title": "Parts List",
            #             "icon": "build_circle",
            #             "link": reverse_lazy("admin:parts_partsmodel_changelist"),
            #         },
            #         {
            #             "title": "Parts Brands",
            #             "icon": "branding_watermark",
            #             "link": reverse_lazy("admin:parts_partsbrand_changelist"),
            #         },
            #         {
            #             "title": "Parts Category",
            #             "icon": "category",
            #             "link": reverse_lazy("admin:parts_partstype_changelist"),
            #         },
            #         {
            #             "title": "Parts Images",
            #             "icon": "image",
            #             "link": reverse_lazy("admin:parts_partsadditionanlimage_changelist"),
            #         },
            #         {
            #             "title": "Parts Videos",
            #             "icon": "video_library",
            #             "link": reverse_lazy("admin:parts_partsvideo_changelist"),
            #         },
            #         {
            #             "title": "Excel File Upload",
            #             "icon": "database_upload",
            #             "link": reverse_lazy("admin:parts_excelfileupload_changelist"),
            #         },
            #     ],
            # },
            # {
            #     "title": "Carts & Orders",
            #     "separator": True,
            #     "collapsible": False,
            #     "items": [
            #         {
            #             "title": "Carts",
            #             "icon": "shopping_cart",
            #             "link": reverse_lazy("admin:cart_cart_changelist"),
            #         },
            #         {
            #             "title": "Cart's Items",
            #             "icon": "view_cozy",
            #             "link": reverse_lazy("admin:cart_cartitem_changelist"),
            #         },
            #         {
            #             "title": "Guest Carts",
            #             "icon": "shopping_cart",
            #             "link": reverse_lazy("admin:cart_guestcart_changelist"),
            #         },
            #         {
            #             "title": "Guest Cart's Items",
            #             "icon": "view_list",
            #             "link": reverse_lazy("admin:cart_guestcartitem_changelist"),
            #         },
            #     ],
            # },
            # {
            #     "title": "Order",
            #     "separator": True,
            #     "collapsible": False,
            #     "items": [
            #         {
            #             "title": "Order Histories",
            #             "icon": "work_history",
            #             "link": reverse_lazy("admin:orders_orderhistory_changelist"),
            #         },
            #         {
            #             "title": "Order Details",
            #             "icon": "receipt_long",
            #             "link": reverse_lazy("admin:orders_orderdetail_changelist"),
            #         },
            #         {
            #             "title": "Coupon",
            #             "icon": "local_activity",
            #             "link": reverse_lazy("admin:cart_coupon_changelist"),
            #         },
            #         {
            #             "title": "Shipping Addresses",
            #             "icon": "add_home_work",
            #             "link": reverse_lazy("admin:shipping_shippingaddress_changelist"),
            #         },
            #         {
            #             "title": "Shipping Fees",
            #             "icon": "currency_exchange",
            #             "link": reverse_lazy("admin:shipping_shippingfee_changelist"),
            #         },
            #     ],
            # },
            # {
            #     "title": "Payment",
            #     "separator": True,
            #     "collapsible": False,
            #     "items": [
            #         {
            #             "title": "Stripe Payment",
            #             "icon": "payments",
            #             "link": reverse_lazy("admin:payment_stripefeeconfig_changelist"),
            #         },
            #     ],
            # },
            # {
            #     "title": "Services",
            #     "separator": True,
            #     "collapsible": False,
            #     "items": [
            #         {
            #             "title": "Reviews",
            #             "icon": "reviews",
            #             "link": reverse_lazy("admin:review_review_changelist"),
            #         },
            #         {
            #             "title": "Messages",
            #             "icon": "business_messages",
            #             "link": reverse_lazy("admin:about_sendmessage_changelist"),
            #         },
            #     ],
            # },
        ],
    },
}

