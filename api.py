from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Usamos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar seguimiento de modificaciones
app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'  # Cambia esto por una clave secreta segura
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Tabla intermedia para la relación muchos a muchos
user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.group_id'), primary_key=True)
)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Campo de contraseña
    # Relación muchos a muchos con los grupos
    groups = db.relationship('Group', secondary=user_group, backref=db.backref('users', lazy='dynamic'))

class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(120), unique=True, nullable=False)
    join_code = db.Column(db.String(120), unique=True, nullable=False)

# Crear las tablas si no existen
@app.before_request
def create_tables():
    db.create_all()

# Rutas para interactuar con los usuarios y grupos
# Obtener todos los usuarios
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'groups': [group.group_name for group in user.groups]  # Lista de grupos del usuario
    } for user in users])

# Obtener un usuario por su ID
@app.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'groups': [group.group_name for group in user.groups]  # Lista de grupos del usuario
    })

# Crear un nuevo usuario
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'user_id': new_user.user_id,
        'username': new_user.username,
        'email': new_user.email
    }), 201

# Crear un nuevo grupo
@app.route('/groups', methods=['POST'])
def add_group():
    data = request.get_json()
    new_group = Group(group_name=data['group_name'], join_code=data['join_code'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify({
        'group_id': new_group.group_id,
        'group_name': new_group.group_name,
        'join_code': new_group.join_code
    }), 201

# Obtener todos los grupos
@app.route('/groups', methods=['GET'])
@jwt_required()
def get_groups():
    groups = Group.query.all()
    return jsonify([{
        'group_id': group.group_id,
        'group_name': group.group_name,
        'join_code': group.join_code
    } for group in groups])

# Obtener un grupo por su ID
@app.route('/groups/<int:group_id>', methods=['GET'])
@jwt_required()
def get_group(group_id):
    group = Group.query.get_or_404(group_id)
    return jsonify({
        'group_id': group.group_id,
        'group_name': group.group_name,
        'join_code': group.join_code
    })

# Asignar un grupo a un usuario
@app.route('/users/<int:user_id>/groups/<int:group_id>', methods=['POST'])
@jwt_required()
def add_user_to_group(user_id, group_id):
    user = User.query.get_or_404(user_id)
    group = Group.query.get_or_404(group_id)
    
    if group not in user.groups:
        user.groups.append(group)
        db.session.commit()
        return jsonify({
            'message': f'User {user.username} added to group {group.group_name}'
        }), 200
    else:
        return jsonify({'message': 'User already in this group'}), 400

# Eliminar un grupo de un usuario
@app.route('/users/<int:user_id>/groups/<int:group_id>', methods=['DELETE'])
@jwt_required()
def remove_user_from_group(user_id, group_id):
    user = User.query.get_or_404(user_id)
    group = Group.query.get_or_404(group_id)
    if group in user.groups:
        user.groups.remove(group)
        db.session.commit()
        return jsonify({
            'message': f'User {user.username} removed from group {group.group_name}'
        }), 200
    else:
        return jsonify({'message': 'User is not a member of this group'}), 400

# Ruta para iniciar sesión y obtener un token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.user_id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401

# Ruta protegida que requiere un token válido
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.username), 200

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)