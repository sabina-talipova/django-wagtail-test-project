from .models import MainMenu

def menus(request):
    header_menu = MainMenu.objects.filter(menu_type="header").first()
    footer_menu = MainMenu.objects.filter(menu_type="footer").first()

    return {
        "header_menu": header_menu,
        "footer_menu": footer_menu,
    }
