{
    "name": "Owl Dashboard",
    "category": "Website",
    "author": "Reusmana",
    "license": "LGPL-3",
    "depends": ["base", "web", "sale", "board"],
    "data": [
        "views/sales_dashboard.xml",
        "views/menu_items.xml",
    ],
    'installable': True,
    'application': True,
    "assets": {
    "web.assets_backend": [
        "owl_dashboard/static/src/components/**/*.js",
        "owl_dashboard/static/src/components/**/*.xml",
        "owl_dashboard/static/src/components/**/*.scss",
        ],
    },

    "sequence": -1,
}
