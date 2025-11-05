from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.snippets.views.snippets import SnippetViewSet
from core.models.data_objects.blog import Blog
from main_menu.models.main_menu import MainMenu

class BlogViewSet(ModelViewSet):
    model = Blog
    icon = "doc-full"
    menu_label = "Blogs"
    add_to_admin_menu = True
    list_display = ["title", "date"]
    search_fields = ["title"]


@hooks.register("register_admin_viewset")
def register_blog_viewset():
    return BlogViewSet()

# class MainMenuViewSet(SnippetViewSet):
#     model = MainMenu
#     icon = "menu"
#     menu_label = "Navigation"
#     add_to_admin_menu = True
#     list_display = ["title"]
#     search_fields = ["title"]
#
#
# @hooks.register("register_admin_viewset")
# def register_mainmenu_viewset():
#     return MainMenuViewSet()
