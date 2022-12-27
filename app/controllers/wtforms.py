from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField,
                     SubmitField, EmailField, TelField,
                     ValidationError, SelectField, TextAreaField)
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
from app.models.model import Tag, ProfileType

#flask wtf
class SignUpForm(FlaskForm):
       username = StringField('Nome',
                            validators=[DataRequired(),
                                          Length(min=3,
                                                 max=150,
                                                 message="Nome inválido"
                                                 )
                                          ]
                            )
       email = EmailField('Email',
                            validators=[DataRequired(),
                                        Email()]
                            )
       password = PasswordField('Senha',
                            validators=[DataRequired(),
                                          Length(min=8,
                                                 message="Sua senha deve ter no mínimo 8 caracteres"
                                                 )
                                          ]
                                   )
       confirm_password = PasswordField('Confirmar Senha',
                                          validators=[DataRequired(),
                                                 EqualTo('password',
                                                        message="Senha diferente da digitada"
                                                        )
                                                 ]
                                          )
       
       submit = SubmitField("Cadastrar-se")
  
       
class LoginForm(FlaskForm):
       email = EmailField('Email',
                            validators=[DataRequired(message="Campo vazio"),
                                        Email()
                                        ]
                            )
       
       password = PasswordField('Password',
                                   validators=[DataRequired(message="Campo vazio")]
                                   )
       
       remember_me = BooleanField('Remember me')
       
       submit = SubmitField("Entrar")


class ProfileForm(FlaskForm):
       
       institucional_name = StringField('Nome da instituição',
                                        validators=[DataRequired(message="Campo vazio")]
                                        )
       cnpj = StringField('cnpj',
                          validators=[DataRequired(message="Campo vazio")]
                          )
       phone = TelField('Telefone de Contato',
                        validators=[DataRequired(message="Campo vazio")]
                        )
       image_file = FileField('Foto de Perfil',
                              validators=[FileAllowed(['jpg', 'png'],
                                                      message='Os tipos de arquivos aceitos são jpg e png')
                                          ],
                              render_kw={"placeholder": "Foto de Perfil"}
                              )
       about = TextAreaField('Descrição',
                                 validators=[Length(max=280,
                                                    message="Limite de 280 caracteres atingido"
                                                    )
                                             ]
                                 )
       profile_type = SelectField('Tipo de Instituição', validate_choice=False)
       
       submit = SubmitField("Sign Up")


class AddressForm(FlaskForm):
       street = StringField('Rua',
                     validators=[DataRequired(message="Campo Vazio"),
                                 Length(min=5,
                                        max=100,
                                        message="Limite de caractere atingido")
                                 ]
                     )
       
       number = StringField('Número',
                            validators=[DataRequired(message="Campo Vazio"),
                                        Length(min=2,
                                               max=4,
                                               message="Limite de caractere atingido"
                                               )
                                        ]
                            )
       
       district = StringField('Estado',
                              validators=[DataRequired(message="Campo Vazio"),
                                          Length(min=2,
                                                 max=30,
                                                 message="Limite de caractere atingido"
                                                 )
                                          ]
                              )
       
       city = StringField('Cidade',
                          validators=[DataRequired(message="Campo Vazio"),
                                      Length(min=2,
                                             max=30,
                                             message="Limite de caractere atingido"
                                             )
                                      ]
                          )
       
       submit = SubmitField("Enviar")
       
class PostForm(FlaskForm):
       title = StringField('Título',
                           validators=[DataRequired(message="Campo vazio")]
                           )
       
       tag = SelectField('Tag',
                         validators=[DataRequired(message="Campo vazio")]
                         )
       
       description = TextAreaField('Descrição',
                                   validators=[Length(max=280,
                                                      message="Limite de 280 caracteres atingido"
                                                      )
                                               ]
                                   )
       
       submit = SubmitField("Enviar")
       
       
#reset
"""       
class UpdateProfileForm(FlaskForm):
       username = StringField('Nome da Instituição',
                            validators=[DataRequired(message = "Campo Vazio" ),
                                          Length(min=3,
                                                 max=150,
                                                 message="Nome inválido"
                                                 )
                                          ]
                            )
       
       email = EmailField('Email da Instituição',
                                  validators=[DataRequired(message="Campo Vazio"),
                                                 Length(max = 150,
                                                        message="Email inválido"
                                                        )
                                                 ]
                                  )
       
       cnpj = StringField('cnpj',
                          validators=[DataRequired(message = "Campo Vazio"),
                                          Length(min = 14,
                                                 max = 14, 
                                                 message = "Cnpj inválido" 
                                                 )
                                          ]
                          )
       
       phone = TelField('Telefonede Contato',
                        validators=[DataRequired(message="Campo Vazio"),
                                          Length(min = 11,
                                                 max = 11,
                                   message= "Telefone inválido")
                                   ]
                        )
       about = StringField('about',
                            validators=[DataRequired(message=""),
                                        Length(max='360')
                                        ]
                            )
       image_file = FileField('Mudar foto de perfil',
                              validators=[FileAllowed(['jpg', 'png'])]
                              )
       street = StringField('Rua',
                            validators=[DataRequired(message="Campo Vazio"),
                                        Length(min=5,
                                               max=100,
                                               message="Limite de caractere atingido")
                                        ]
                            )
       number = StringField('Número',
                            validators=[DataRequired(message="Campo Vazio"),
                                        Length(min=2,
                                               max=4,
                                               message="Limite de caractere atingido"
                                               )
                                        ]
                            )
       district = StringField('Estado',
                              validators=[DataRequired(message="Campo Vazio"),
                                          Length(min=2,
                                                 max=30,
                                                 message="Limite de caractere atingido"
                                                 )
                                          ]
                              )
       city = StringField('Cidade',
                          validators=[DataRequired(message="Campo Vazio"),
                                      Length(min=2,
                                             max=30,
                                             message="Limite de caractere atingido"
                                             )
                                      ]
                          )
       
       
       def validate_username(self, username):
              if username.data != current_user.username:
                     user = User.query.filter_by(username=username.data).first()
                     if user:
                            raise ValidationError("Esse usuário já existe.")
       
       
       
       def validate_email(self, email):
              if email.data != current_user.email:
                     user = User.query.filter_by(email=email.data).first()
                     if user:
                            raise ValidationError("Já existe uma conta com esse email.")
                     
       
       def validate_cnpj(self, email):
              if email.data != current_user.email:
                     user = User.query.filter_by(email=email.data).first()
                     if user:
                            raise ValidationError("Já existe uma conta com esse email.")
                     
                       
       def validate_image_file(self, email):
              if email.data != current_user.email:
                     user = User.query.filter_by(email=email.data).first()
                     if user:
                            raise ValidationError("Já existe uma conta com esse email.")  
       
       
       def validate_street(self, email):
              if email.data != current_user.email:
                     user = User.query.filter_by(email=email.data).first()
                     if user:
                            raise ValidationError("Já existe uma conta com esse email.")  
       
       
       def validate_number(self, email):
              if email.data != current_user.email:
                     user = User.query.filter_by(email=email.data).first()
                     if user:
                            raise ValidationError("Já existe uma conta com esse email.")
                                           
              
              
class RequestResetForm(FlaskForm):
       email= StringField("Email",
                            validators= [DataRequired(), Email()])
       submit = SubmitField("Pedido de reinicialização")

       def validate_email(self, email):
              user = User.query.filter_by(email=email.data).first()
              if user is None:
                     raise ValidationError('Não há uma conta registrada com esse email.')



class ResetPasswordForm(FlaskForm):
       password = PasswordField('Senha',
                                validators=[DataRequired(),
                                            Length(min=8,
                                                   message="Sua senha deve ter no mínimo 8 caracteres"
                                                   )
                                            ]
                                )
       
       confirm_password = PasswordField('Confirmar Senha',
                                          validators=[DataRequired(),
                                                 EqualTo('password',
                                                        message="Senha diferente da digitada"
                                                        )
                                                 ]
                                          )
       submit = SubmitField("")


class AddressForm(FlaskForm):
       street = StringField('Rua',
                            validators=[DataRequired(message="Campo Vazio"),
                                        Length(min=5,
                                               max=100,
                                               message="Limite de caractere atingido"
                                               )
                                        ]
                            )
       number = StringField('Número',
                            validators=[DataRequired(message="Campo Vazio"),
                                        Length(min=2,
                                               max=4,
                                               message="Limite de caractere atingido"
                                               )
                                        ]
                            )
       district = StringField('Estado',
                              validators=[DataRequired(message="Campo Vazio"),
                                          Length(min=2,
                                                 max=30,
                                                 message="Limite de caractere atingido"
                                                 )
                                          ]
                              )
       city = StringField('Cidade',
                          validators=[DataRequired(message="Campo Vazio"),
                                      Length(min=2,
                                             max=30,
                                             message="Limite de caractere atingido"
                                             )
                                      ]
                          )


"""









"""
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    extra = db.Column(db.String(50))

    def __repr__(self):
        return '[Choice {}]'.format(self.name)

def choice_query():
    return Choice.query

class ChoiceForm(FlaskForm):
    opts = SelectField(query_factory=choice_query, allow_blank=False, get_label='name')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ChoiceForm()

    form.opts.query = Choice.query.filter(Choice.id > 1)

    if form.validate_on_submit():
        return '<html><h1>{}</h1></html>'.format(form.opts.data)

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)"""
