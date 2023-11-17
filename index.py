import os
from flask import Flask, render_template, redirect, request, url_for, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import pymysql


app = Flask("project")
mysql=MySQL()
db=MySQL(app)

if __name__ == '__main__':
   app.config.from_object(['development'])
   app.run()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'productos'
mysql.init_app()

@app.route('/home')
def principal():
   return render_template('index.html')

@app.route('/', metods=['GET'])
def index():
   return redirect(url_for('login.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      print(request.form['username'])
      print(request.form['password'])
      return render_template('/login.html')
   else:
      return render_template('/login.html')
      
@app.route('/quienesomos')
def quienesomos():
   return render_template('quienesomos.html')

@app.route('/contacto')
def contacto():
   conexion=mysql.connect()
   cursor=conexion.cursor()
   cursor.execute("SELECT * FROM `Contactos`")
   contactos=cursor.fetchall()
   conexion.commit()
   print(contactos)

   return render_template('contacto.html')

@app.route('/contacto/guardar', methods=['POST'])
def contacto_guardar():
   if request.method == 'POST':
      _nombre=request.form['name']
      _email=request.form['email']
      _asunto=request.form['subject']
      _mensaje=request.form['message']
      conexion=mysql.connect()
      cursor=conexion.cursor()
      cursor.execute('INSERT INTO `Contactos` (`Nombre`, `Email`, `Asunto`, `Mensaje`) VALUES (%s, %s, %s, %s)', (_nombre, _email, _asunto, _mensaje))
      conexion.commit()

      print(_nombre)
      print(_email)
      print(_asunto)
      print(_mensaje)

      return render_template('contacto.html')

@app.route('/nuestrosaliados')
def nuestrosaliados():
   return render_template('nuestrosaliados.html')

@app.route('/ProdServ')
def ProdServ():
   conexion=mysql.connect()
   cursor=conexion.cursor()
   cursor.execute("SELECT * FROM `Products`")
   products=cursor.fetchall()
   conexion.commit()
   
   return render_template('ProdServ.html', products=products)

@app.route('/compras')
def compras():
   conexion=mysql.connect()
   cursor=conexion.cursor()
   cursor.execute("SELECT * FROM `Envio`")
   envio=cursor.fetchall()
   conexion.commit()
   print(envio)
   return render_template('compras.html')

@app.route('/compras/guardar', methods=['POST'])
def compras_guardar():
   if request.method == 'POST':
      _first_name=request.form['firstName']
      _last_name=request.form['lastName']
      _username=request.form['username']
      _email=request.form['email']
      _adress=request.form['adress']
      _zip=request.form['zip']
      conexion=mysql.connect()
      cursor=conexion.cursor()
      cursor.execute('INSERT INTO `Envio`(`Nombre`, `Apellido`, `Nombre de usuario`, `Email`, `Dirección de envio` , `CP`) VALUES (%s, %s, %s, %s, %s, %s)', (_first_name, _last_name, _username, _email, _adress, _zip))
      conexion.commit()

      print(_first_name)
      print(_last_name)
      print(_username)
      print(_email)
      print(_adress)
      print(_zip)

   return 'recived'

@app.route('/img/<imagen>')
def imagenes(imagen):
   print(imagen)
   return send_from_directory (os.path.join('./templates/img'), imagen)

@app.route("/css/<archivocss>")
def css_link(archivocss):
   return send_from_directory(os.path.join('templates/css'), archivocss)

@app.route('/admin/products')
def admin_products():
   conexion=mysql.connect()
   cursor=conexion.cursor()
   cursor.execute("SELECT * FROM `Products`")
   products=cursor.fetchall()
   conexion.commit()
   print(products)
   return render_template('admin/products.html', products=products)

@app.route('/admin/products/guardar', methods=['POST'])
def admin_products_guardar():
   _nombre=request.form['txtNombre']
   _descripcion=request.form['txtDescripcion']
   _archivo=request.files['txtImagen']
   _precio=request.form['txtPrecio']

   tiempo=datetime.now()
   horaActual=tiempo.strftime('%Y%H%M%S')

   if _archivo.filename!="":
      nuevoNombre=horaActual + "_" + _archivo.filename
      _archivo.save("./img" + nuevoNombre)

   sql="INSERT INTO `Products` (`ID`, `Nombre`, `Imagen`, `Descripción del producto`, `Precio`) VALUES (NULL, %s, %s, %s, %s);"
   datos=(_nombre, nuevoNombre, _descripcion, _precio)
   conexion=mysql.connect()
   cursor=conexion.cursor()
   cursor.execute(sql, datos)
   conexion.commit()
   print(_nombre)
   print(_descripcion)
   print(_archivo)
   print(_precio)
   
   return redirect('/admin/products')

@app.route('/admin/products/borrar', methods=['POST'])
def admin_products_borrar():
   _id=request.form['txtID']
   print(_id)
   
   conexion=mysql.connect()
   cursor=conexion.cursor()
   cursor.execute("SELECT imagen FROM `Products` WHERE id=%s", (_id  ))
   product=cursor.fetchall()
   conexion.commit()
   print(product)

   if os.path.exists("/templates/img/"+str(product[0][0])):
      os.unlink("/templates/img/"+str(product[0][0]))

   conexion=mysql.connect()
   cursor=conexion.cursor()
   cursor.execute("DELETE  FROM `Products` WHERE id=%s", (_id))
   conexion.commit()
   return redirect('/admin/products')

@app.route('/buscar-producto', methods=['GET', 'POST'])
def BuscarProducto():
   if request.method == "POST":
      search = request.form['buscar']
      conexion=mysql.connect()
      cursor=conexion.cursor()
      sql=cursor.execute("SELECT * FROM `Products` WHERE Nombre='%s' ORDER BY ID DESC" % (search,))
      resultadoBusqueda = cursor.fetchone()
      cursor.close()
      conexion.close()
      return render_template('/resultadoBusqueda.html', Data=resultadoBusqueda , busqueda=search)
   return redirect (url_for('index'))

@app.route('/compras/guardar')
def products ():
   try:
      conn = mysql.connect()
      cursor = conn.cursor(pymysql.cursors.DictCursor)
      cursor.execute("SELECT * FROM `Products`")
      rows=cursor.fetchall()
      return render_template('products.html', products=rows)
   except Exception as e:
      print (e)
   finally:
      cursor.close()
      conn.close()

@app.route('/add', methods=['POST'])
def add_product_cart():
   try:
      _quantity=int(request.form['_quantity'])
      _id=request.form[id]
      if _quantity and request.method == "POST":
         conn = mysql.connect()
         cursor = conn.cursor(pymysql.cursors.DictCursor)
         cursor.execute("SELECT * FROM `Products` WHERE ID='%s'", _id)
         row=cursor.fetchone()

         itemArray = {row['ID'] : {'Nombre':row['Nombre'], 'Imagen':row['Imagen'], 'Descripción del producto':row['Descripción del producto'], 'quantity':_quantity, 'Precio':row['Precio'], 'total':_quantity*row['Precio'] } }
         all_total_price=0
         all_total_quantity=0

         session.modified = True
         if 'cart_item' in session:
            if row['code'] in session ['cart_item']:
               for key, value in session ['cart_item'].items():
                if row['code']  == key: 
                   old_quantity = session['cart_item'][key]['_quantity']
                   total_quantity = old_quantity + _quantity
                   session['cart_item'][key]['_quantity']=total_quantity
                   session['cart_item'][key]['total_price']=total_quantity*row['Precio']
            else: 
               session['cart_item']=array_merge(session['cart_item'], itemArray)
               for key, value in session ['cart_item'].items():
                  individual_quantity=int(session ['cart_item'][key]['_quantity'])
                  individual_price=float(session ['cart_item'][key]['total_price'])
                  all_total_quantity=all_total_quantity+individual_quantity
                  all_total_price=all_total_price+individual_price
         else: 
            session ['cart_item'] = itemArray 
            all_total_quantity = all_total_quantity+_quantity
            all_total_price = all_total_price+_quantity*row['Precio'] 

         session['all_total_quantity'] = all_total_quantity
         session['all_total_price'] = all_total_price 

         return redirect(url_for('products'))
      else:
         return 'Error al añadir producto al carro de compras'
   except Exception as e:
      print (e)
   finally:
      cursor.close()
      conn.close()
   return render_template('compras.html')

@app.route('/empty')
def empty_cart():
   try:
      session.clear()
      return redirect(url_for('compras'))
   except Exception as e:
      print(e)

@app.route('/delete/<string:code>')
def delete_product(code):
   try:

      all_total_price=0
      all_total_quantity=0
      session.modified=True
      
      for item in session['cart_item'].items():
         if item[0]==code:
            session['cart_item'].pop(item[0], None)
         if 'cart_item' in session:
            for key, value in session['cart_item'].items():
               individual_quantity=int(session ['cart_item'][key]['_quantity'])
               individual_price=float(session ['cart_item'][key]['total_price'])
               all_total_quantity=all_total_quantity+individual_quantity
               all_total_price=all_total_price+individual_price
         break
      if all_total_quantity == 0:
         session.clear()
      else:
         session['all_total_quantity']=all_total_quantity
         session['all_total_price']=all_total_price
      return redirect(url_for('compras'))
   except Exception as e:
      print(e)

def array_merge(first_array, second_array):
   if isinstance (first_array, list) and isinstance (second_array, list):
      return first_array + second_array
   elif isinstance (first_array, dict) and isinstance (second_array, dict):
      return dict(list(first_array.items())+list(second_array.items()))
   elif isinstance (first_array, set) and isinstance (second_array, set):
      return first_array.union(second_array)
   return False

@app.errorhandler(404)
def not_found(error):
   return redirect(url_for('index'))



