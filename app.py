
from flask import Flask, render_template, request, redirect ,url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'kiskodb'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/home')
def Home():
    return render_template('index.html')

@app.route('/gestion_proyectos.html')
def GestionProyectos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM project')
    data = cur.fetchall()
    
    return render_template('gestion_proyectos.html', projects = data)


@app.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO project (name, description) VALUES (%s, %s)', (name, description))
        mysql.connection.commit()

        flash("Proyecto agregado correctamente")

        return redirect(url_for('GestionProyectos'))

@app.route('/edit_project/<id>')
def get_project(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM project WHERE id = %s', [id])
    data = cur.fetchall()

    print(data[0])
    
    return render_template('edit_project.html', project = data[0])

@app.route('/update_project/<id>', methods=['POST'])
def update_project(id):
    if request.method == 'POST':
        
        name = request.form['name']
        description = request.form['description']

        cur = mysql.connection.cursor()   
        cur.execute("""
            UPDATE project
            SET name = %s,
            description = %s
            WHERE id = %s
        """, (name, description, id))
        mysql.connection.commit()       
        
        flash('Proyecto actualizado correctamente')

        return redirect(url_for('GestionProyectos'))
    

@app.route('/delete_project/<string:id>')
def delete_project(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM project WHERE id = {0}'.format(id))
    mysql.connection.commit()

    flash("Proyecto eliminado correctamente")
    return redirect(url_for('GestionProyectos'))
    

if __name__ == '__main__':
    app.run(port=3000, debug=True)