from flask_admin import Admin
from flask_admin.base import AdminIndexView
#from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask import redirect, url_for
from flask_login import login_required, current_user
from app.models.model import (Address, Post, Profile,
                              ProfileType, Tag, Role,
                              User
                              )


AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
sqla.ModelView._handle_view = login_required(sqla.ModelView._handle_view)
admin = Admin()


class UserAdmin(sqla.ModelView):
    
    
    @login_required
    def is_accessible(self):
        try:
            if current_user and (current_user.roles.role == "Admin"):
                return current_user.is_authenticated
                    
        except:
            return '401'
        
        
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('/login'))


def admin_views():
    # list_views = [User, Profile, type, Post, Tag, ProfileType, Address] -> problema ao colocar no add_views
    from app.models import db
    admin.add_views(UserAdmin(User, db.session))
    admin.add_view(UserAdmin(Role, db.session))
    admin.add_view(UserAdmin(Profile, db.session))
    admin.add_view(UserAdmin(ProfileType, db.session))
    admin.add_view(UserAdmin(Address, db.session))
    admin.add_view(UserAdmin(Post, db.session))
    admin.add_view(UserAdmin(Tag, db.session))
    #admin.add_view(ModelView('401',db.session)) -> tela de erro

