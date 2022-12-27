from datetime import datetime
from app import bcrypt, db, login_manager
from flask_login import UserMixin
from sqlalchemy import event
from itsdangerous import TimedSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    username = db.Column(db.String(150),
                         nullable=False
                         )
    email = db.Column(db.String(150),
                      unique=True,
                      nullable=False
                      )
    password = db.Column(db.String(200),
                         nullable=False
                         )
    id_profile = db.relationship('Profile',
                                 backref='users',
                                 lazy=True
                                 )
    role_id = db.Column(db.Integer,
                        db.ForeignKey('roles.id'),
                        nullable=False,
                        default=3
                        )
    
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
        
    def __repr__(self):
        return f'User {self.username}'


    def verify_password(self, pwd):
        verified = bcrypt.check_password_hash(self.password, pwd)
        return verified
    
    
    def get_reset_token(self, expires_sec=3600):
        serialize = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serialize.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        serialize = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serialize.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User: {self.username}, {self.email}"


#verifica encriptação 
@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return bcrypt.generate_password_hash(value)
    return value
        

class Role(db.Model):
    __tablename__ = "roles"
    
    id = db.Column('id',
                   db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    role = db.Column('role',
                     db.String(10),
                     nullable=False
                     )
    
    user_id = db.relationship('User',
                              backref='roles',
                              lazy=True
                              )
    
    
    def __repr__(self):
        return f'{self.role}'
    
    
class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False
                        )
    institucional_name = db.Column('institucional_name',
                                   db.String(150),
                                   unique=True,
                                   nullable=False
                                   )
    cnpj = db.Column('cnpj',
                     db.String(14),
                     unique=True,
                     nullable=False
                     )
    phone = db.Column('phone',
                      db.String(11),
                      nullable=False
                      )
    about = db.Column('about',
                        db.String(280),
                        nullable=True
                        )
    image_file = db.Column(db.String(20),
                           nullable=True,
                           default= 'logo_vazada.png'
                           )
    posts = db.relationship('Post',
                              backref='profiles',
                              lazy=True
                              )
    address = db.Column(db.Integer,
                        db.ForeignKey('adresses.id'),
                        nullable=True
                        )
    profile_type = db.Column(db.Integer,db.ForeignKey('profile_types.id'),
                             nullable=True
                             )  
        
    def __repr__(self):
        return f'{self.user_id}'
    
    

#tipo de instituição
class ProfileType(db.Model):
    __tablename__ = "profile_types"
    
    id = db.Column('id',
                   db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    types = db.Column('types',
                     db.String(30),
                     nullable=False
                     )
    profile_id = db.relationship('Profile',
                                 backref='profile_types',
                                 lazy=True
                                 )
    

    def __repr__(self):
        return self.id, self.types
      
    
#endereço
class Address(db.Model):
    __tablename__ = "adresses"
    
    id = db.Column('id',
                   db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    street = db.Column('street',
                     db.String(100),
                     nullable=False
                     )
    number = db.Column('number',
                       db.String(4),
                       nullable=False
                      )
    district = db.Column('district',
                         db.String(30),
                         nullable=False
                         )
    city = db.Column('city',
                     db.String(30),
                     nullable=False
                     )
    profile_id = db.relationship('Profile',
                                 backref='adresses',
                                 lazy=True
                                 )


    def __repr__(self):
        return f'street {self.street}; number {self.number}; district {self.district}; and city {self.city}'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    title = db.Column(db.String(50),
                            nullable=False
                            )  
    description = db.Column(db.Text,
                            nullable=False
                            )
    pub_date = db.Column(db.DateTime,
                         nullable=False,
                         default=datetime.utcnow
                         )
    profile_id = db.Column(db.Integer,
                            db.ForeignKey('profiles.id'),
                            nullable=False
                            ) 
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       nullable=False
                       ) 
    

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    tag = db.Column('tag',
                    db.String(50),
                    nullable=False
                    )
    id_post = db.relationship('Post',
                              backref='tags',
                              lazy=True
                              )


    def __repr__(self):
        return f'{self.tag}'