import os


def main():     
    
    
    from app import app_config
    
    app = app_config() 
    
    
    from app import (db, login_manager, bcrypt)
    bcrypt.init_app(app)        #flask-bcrypt
    db.init_app(app)            #flask-SQLAlchemy
    login_manager.init_app(app) #flask-Login
    
    
    from app.web import register_routes
    register_routes(app)
    

    with app.app_context(): 
        db.create_all()    
        

    from app.admin import admin
    admin.name = 'PAD'
    admin.template_mode = 'bootstrap3'
    admin.init_app(app)
    
    
    from app.admin import admin_views
    admin_views()


    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()