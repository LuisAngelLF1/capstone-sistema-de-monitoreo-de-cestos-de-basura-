import mysql.connector
 
#Conexión con el servidor MySQL Server
conexionMySQL = mysql.connector.connect(
    host='localhost',
    user='luis',
    passwd='',
    db='lista_compra'
)
 
#Pedimos al usuario el nombre y la cantidad del artículo que se insertará en la BD MySQL
sol_nombre = input("Introduzca el nombre del artículo: ")
sol_cantidad = int(input("Introduzca la cantidad de unidades en stock del artículo: "))
 
#Consulta SQL que ejecutaremos, en este caso un insert
sqlInsertarRegistro = f"""INSERT INTO articulos (nombre, cantidad) VALUES ("{sol_nombre}", {sol_cantidad})"""
#Establecemos un cursor para la conexión con el servidor MySQL
cursor = conexionMySQL.cursor()
#A partir del cursor, ejecutamos la consulta SQL de inserción
cursor.execute(sqlInsertarRegistro)
conexionMySQL.commit()
 
#Consulta de selección para mostrar los registros por pantalla
#para comprobar que se ha insertado uno nuevo
sqlSelect = """SELECT nombre, cantidad
           FROM articulos
           """
#A partir del cursor, ejecutamos la consulta SQL
cursor.execute(sqlSelect)
#Guardamos el resultado de la consulta en una variable
resultadoSQL = cursor.fetchall()
#Cerramos el cursor y la conexión con MySQL
cursor.close()
conexionMySQL.close()
#Mostramos el resultado por pantalla
print (resultadoSQL)