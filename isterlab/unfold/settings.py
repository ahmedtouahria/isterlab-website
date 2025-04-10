from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static


UNFOLD = {
    "SITE_TITLE": "Admin panel",
    "SITE_HEADER": "Admin panel",
    "SITE_URL": "/",
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True
   # "DASHBOARD_CALLBACK": "qateeb.unfold.views.dashboard_callback",

    "SITE_ICON": {
        "light": lambda request: static("assets/images/logo/icon.ico"),  # light mode
        "dark": lambda request: static("assets/images/logo/icon.ico"),  # dark mode
    },
        "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("app/smartinvoice-fav.png"),
        },
    ],
  #  "DASHBOARD_CALLBACK": "Smart invoice.unfold.views.dashboard_callback",
    "COLORS": {
    "primary": {
        "50": "240 248 255",  # AliceBlue
        "100": "230 230 250",  # Lavender
        "200": "176 224 230",  # PowderBlue
        "300": "135 206 235",  # SkyBlue
        "400": "100 149 237",  # CornflowerBlue
        "500": "70 130 180",  # SteelBlue
        "600": "30 144 255",  # DodgerBlue
        "700": "0 0 128",  # Navy
        "800": "25 25 112",  # MidnightBlue
        "900": "0 0 139",  # DarkBlue
        "950": "0 0 205",  # MediumBlue
    },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Global"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },

                    {
                        "title": _("Configurations"),
                        "icon": "settings",  # Supported icon set: https://fonts.google.com/icons
                        "link":"/admin/constance/config/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
           { "title": _("Portal"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Blogs"),
                        "icon": "rate_review",  # Supported icon set: https://fonts.google.com/icons
                        "link":"/admin/landing/blog/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Brands"),
                        "icon": "hotel_class",  # Supported icon set: https://fonts.google.com/icons
                        "link":"/admin/landing/brand/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Partners"),
                        "icon": "handshake",  # Supported icon set: https://fonts.google.com/icons
                        "link":"/admin/landing/contactpartner/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Coverages"),
                        "icon": "radar",  # Supported icon set: https://fonts.google.com/icons
                        "link":"/admin/landing/coverage/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Faq's"),
                        "icon": "unknown_document",  # Supported icon set: https://fonts.google.com/icons
                        "link":"/admin/landing/faq/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Services"),
                        "icon": "home_repair_service",  # Supported icon set: https://fonts.google.com/icons
                        "link":"/admin/landing/service/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Solutions"),
                        "icon": "category",  # Supported icon set: https://fonts.google.com/icons
                        "link":"/admin/landing/solution/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                {
                        "title": _("Contact's"),
                        "icon": "message",  # Supported icon set: https://fonts.google.com/icons
                        "link":"/admin/landing/contact/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    ]
                    
                    },

        ],
    },
}