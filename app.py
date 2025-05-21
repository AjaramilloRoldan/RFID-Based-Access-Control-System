from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import mysql.connector
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Conexión a la base de datos MySQL
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Roldan.1982",
        database="control_acceso"
    )

# Configuración SQLAlchemy para MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Roldan.1982@localhost:3306/control_acceso'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos SQLAlchemy
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rfid = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    logs = db.relationship('AccessLog', backref='user', lazy=True)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class AccessLog(db.Model):
    __tablename__ = 'access_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Valor predeterminado
    success = db.Column(db.Boolean, default=True)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Login común para Admin y Usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                session.clear()
                session['user_id'] = user['id']
                session['role'] = 'user'
                return redirect(url_for('instalaciones'))

            cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
            admin = cursor.fetchone()
            if admin:
                session.clear()
                session['user_id'] = admin['id']
                session['role'] = 'admin'
                return redirect(url_for('dashboard'))

            cursor.close()
            conn.close()
        except Exception as e:
            cursor.close()
            conn.close()
            return f"Error en el login: {str(e)}", 500

    return render_template('login.html')


#dashboard
@app.route('/dashboard')
def dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    admin_name = "Administrador"  # Aquí obtén el nombre real del admin, p. ej. desde la sesión o BD
    return render_template('dashboard.html', admin_name=admin_name)


# Instalaciones para usuario
@app.route('/instalaciones')
def instalaciones():
    if session.get('role') != 'user':
        return redirect(url_for('login'))
    lista = [
    {
        'nombre': 'Auditorio Principal',
        'desc': 'Un amplio auditorio con capacidad para 300 personas, equipado con tecnología de sonido y proyección de última generación.',
        'imagen': 'https://cdn.pixabay.com/photo/2013/02/26/01/10/auditorium-86197_1280.jpg'
    },
    {
        'nombre': 'Sala de Reuniones',
        'desc': 'Sala moderna para reuniones de hasta 20 personas, con pizarra digital y videoconferencia.',
        'imagen': 'https://cdn.pixabay.com/photo/2017/08/23/16/05/iocenters-2673327_1280.jpg'
    },
    {
        'nombre': 'Gimnasio',
        'desc': 'Gimnasio completamente equipado con máquinas de cardio, pesas y área de entrenamiento funcional.',
        'imagen': 'https://cdn.pixabay.com/photo/2020/04/09/16/35/fitness-5022191_1280.jpg'
    },
    {
        'nombre': 'Cafetería',
        'desc': 'Cafetería acogedora que ofrece una variedad de comidas y bebidas, ideal para relajarse y socializar.',
        'imagen': 'https://cdn.pixabay.com/photo/2020/10/07/12/33/cafe-5635015_1280.jpg'
    },
    {
        'nombre': 'Laboratorio de Innovación',
        'desc': 'Espacio dedicado a la investigación y desarrollo, equipado con tecnología avanzada.',
        'imagen': 'https://cdn.pixabay.com/photo/2022/09/10/22/09/science-lab-7445779_1280.jpg'
    },
    {
        'nombre': 'Terraza al Aire Libre',
        'desc': 'Una hermosa terraza con vistas panorámicas, perfecta para eventos al aire libre y actividades recreativas.',
        'imagen': 'https://cdn.pixabay.com/photo/2021/07/20/06/08/balcony-6479819_1280.jpg'
    },
    {
        'nombre': 'Estudio de Grabación',
        'desc': 'Estudio profesional para grabación de audio y video, con equipos de alta calidad y personal especializado.',
        'imagen': 'https://cdn.pixabay.com/photo/2016/03/30/05/41/music-1290087_1280.jpg'
    },
    {
        'nombre': 'Sala de Capacitación',
        'desc': 'Sala equipada con tecnología de enseñanza, ideal para talleres y cursos de formación.',
        'imagen': 'https://cdn.pixabay.com/photo/2015/01/08/18/11/laptops-593296_1280.jpg'
    },
     {
        'nombre': 'Biblioteca',
        'desc': 'Una amplia biblioteca con miles de libros, áreas de estudio y salas de lectura silenciosa.',
        'imagen': 'https://cdn.pixabay.com/photo/2014/10/14/20/14/library-488690_1280.jpg'
    }
    
]



    return render_template('instalaciones.html', instalaciones=lista)

# Endpoint para registrar y mostrar historial
@app.route('/historial', methods=['GET', 'POST'])
def historial():
    if request.method == 'POST':
        try:
            data = request.get_json()
            uid = data.get('uid')

            if not uid:
                return jsonify({"error": "Identificación no proporcionada"}), 400

            conn = get_db()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE rfid = %s", (uid,))
            user = cursor.fetchone()

            if user:
                # Insertar con el valor predeterminado para timestamp
                cursor.execute("INSERT INTO access_log (user_id, success) VALUES (%s, %s)", (user['id'], True))
                conn.commit()
                response = {'message': 'Acceso autorizado', 'uid': uid}
            else:
                # Insertar con el valor predeterminado para timestamp
                cursor.execute("INSERT INTO access_log (user_id, success) VALUES (%s, %s)", (None, False))
                conn.commit()
                response = {'message': 'Acceso denegado', 'uid': uid}

            cursor.close()
            conn.close()
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": f"Error procesando identificación: {str(e)}"}), 500

    # Solicitud GET - mostrar historial (solo admin)
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            access_log.id AS id,
            COALESCE(users.name, 'UID no registrado') AS usuario,
            access_log.timestamp AS fecha,
            CASE 
                WHEN access_log.success = 1 THEN '✅ Autorizado'
                ELSE '❌ Denegado'
            END AS estado
        FROM access_log
        LEFT JOIN users ON access_log.user_id = users.id
        ORDER BY access_log.timestamp DESC
    """)
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('historial.html', logs=logs)

# Mostrar usuarios (solo admin)
@app.route('/usuarios')
def usuarios():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

# Agregar usuario (solo admin)
@app.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        rfid = request.form.get('rfid')
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([name, rfid, username, password]):
            return "Todos los campos son obligatorios", 400

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, rfid, username, password) VALUES (%s, %s, %s, %s)",
                (name, rfid, username, password)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            return f"Error agregando usuario: {str(e)}", 500

        return redirect(url_for('usuarios'))

    return render_template('agregar_usuario.html')

# Editar usuario (solo admin)
@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    usuario = cursor.fetchone()

    if request.method == 'POST':
        name = request.form.get('name')
        rfid = request.form.get('rfid')
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            cursor.execute(
                "UPDATE users SET name=%s, rfid=%s, username=%s, password=%s WHERE id=%s",
                (name, rfid, username, password, id)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            cursor.close()
            conn.close()
            return f"Error actualizando usuario: {str(e)}", 500

        return redirect(url_for('usuarios'))

    cursor.close()
    conn.close()
    return render_template('editar_usuario.html', usuario=usuario)

# Eliminar usuario (solo admin)
@app.route('/eliminar_usuario/<int:user_id>')
def eliminar_usuario(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return f"Error eliminando usuario: {str(e)}", 500

    return redirect(url_for('usuarios'))

# Cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
