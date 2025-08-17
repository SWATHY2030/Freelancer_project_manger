import mysql.connector

def connect_db():
    con = mysql.connector.connect(
        host="localhost",
        user="root",        
        password="Swathy@303",  
        database="Freelancer_db"  
    )
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            client_name VARCHAR(255),
            project_title VARCHAR(255),
            fee FLOAT,
            deadline DATE,
            status VARCHAR(50))
    """)
    con.commit()
    con.close()

def insert_project(client, title, fee, deadline, status):
    con = mysql.connector.connect(
        host="localhost",
        user="root",        
        password="Swathy@303",  
        database="Freelancer_db"  
    )
    cur = con.cursor()
    cur.execute("INSERT INTO projects (client_name, project_title, fee, deadline, status) VALUES (%s, %s, %s, %s, %s)",
                (client, title, fee, deadline, status))
    con.commit()
    con.close()

def fetch_all():
    con = mysql.connector.connect(
        host="localhost",
        user="root",        
        password="Swathy@303",  
        database="Freelancer_db"  
    )
    cur = con.cursor()
    cur.execute("SELECT * FROM projects")
    rows = cur.fetchall()
    con.close()
    return rows

def search_projects(keyword):
    con = mysql.connector.connect(
        host="localhost",
        user="root",        
        password="Swathy@303",  
        database="Freelancer_db"  
    )
    cur = con.cursor()
    cur.execute("SELECT * FROM projects WHERE client_name LIKE %s OR status LIKE %s",
                ('%' + keyword + '%', '%' + keyword + '%'))
    rows = cur.fetchall()
    con.close()
    return rows

def delete_project(project_id):
    con = mysql.connector.connect(
        host="localhost",
        user="root",        
        password="Swathy@303",  
        database="Freelancer_db"  
    )
    cur = con.cursor()
    cur.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    con.commit()
    con.close()
