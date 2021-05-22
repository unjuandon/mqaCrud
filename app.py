from flask import Flask, render_template, request, url_for, redirect, flash
from flask.globals import request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'root'

app.config['MYSQL_DB'] = 'mqa-app'

mysql = MySQL(app)

app.secret_key='mysecret'


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    print(data)
    return render_template ("index.html", usuarios=data)

@app.route('/añadir', methods=['POST'])
def añadir():
    if request.method == 'POST':
        fullname= request.form['fullname']
        phone= request.form['phone']
        email= request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (fullname, phone, email) VALUES (%s, %s ,%s)', (fullname,phone,email) )
        mysql.connection.commit()       
        flash("usuario añadido satistactoriamente") 
        return redirect(url_for('index'))
        
        

@app.route('/editar/<id>')
def editar(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('/editar.html', usuario=data[0])



@app.route('/actualizar/<id>', methods = ['POST'])
def actualizar(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
                UPDATE users
                SET fullname = %s,
                email = %s,
                phone = %s
                WHERE id = %s
                """, (fullname,phone,email,id))
        mysql.connection.commit()
        flash('Se actualizaron los datos de usuario')
        return redirect(url_for('index'))
    
    

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id ={0}'.format(id))
    mysql.connection.commit()
    flash('Usuario eliminado')
    return redirect(url_for('index'))
    
    
   



if __name__ == '__main__':   
    app.run(debug= True, port=5000)

