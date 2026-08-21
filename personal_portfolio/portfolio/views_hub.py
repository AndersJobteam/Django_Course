from .views.home_views import home
from .views.project_views import projects, project_detail, delete_comment
from .views.account_views import account, account_logout

__all__ = [
    'home',
    'projects',
    'project_detail',
    'delete_comment',
    'account',
    'account_logout'
]