# export FLASK_APP=web_gui.py
# flask run --host=0.0.0.0

#navigation buttons
#add cols
#del cols
#edit row data
#search
#hardcoded host, user, password


from flask import Flask
from flask import render_template
from flask import request
import re
import my_crud

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/database", methods=['POST', 'GET'])
def database():

    if request.method == 'POST':
        if 'dbname' in request.form:
            my_crud.create_db("127.0.0.1", "root", "xxxxxxxx", request.form['dbname'])
        if 'delete' in request.form:
            my_crud.drop_db("127.0.0.1", "root", "xxxxxxxx", request.form['delete'])

    delete_db_form1 = '<form action="/database" method="post" style="display: inline;"><input type="hidden" name="delete" value="'
    delete_db_form2 = '"><input type="image" src="static/delete.png" alt="Submit"></form>'

    list_table_form1 = '<form action="/table-list" method="post" style="display: inline;"><input type="hidden" name="dbname" value="'
    list_table_form2 = '"><input type="image" src="static/menu.png" alt="Submit"></form>'

    junk2 = my_crud.list_dbs("127.0.0.1", "root", "xxxxxxxx")
    db_list = "<table>"
    for i in junk2:
        db_list = db_list + "<tr><td>" + delete_db_form1 + i[0] + delete_db_form2 + list_table_form1 + i[0] + list_table_form2 + i[0] + "</td></tr>"
    db_list = db_list + "</table>"
    return render_template('database.html', db_list=db_list)


@app.route("/table-list", methods=['POST', 'GET'])
def table_list():

    db_name = ""
    if request.method == 'POST':

        if 'dbname' in request.form:
            db_name = request.form['dbname']
        else:
            return "No DB name set"

        if 'action' in request.form:

            if 'action' in request.form:
                if request.form['action'] == 'delete':
                    if 'table-name' in request.form:
                        my_crud.drop_table("127.0.0.1", "root", "xxxxxxxx", db_name, request.form['table-name'])

                if request.form['action'] == 'create':
                    if 'table-name' in request.form and 'table-fields' in request.form:
                        p1 = re.compile(r',')
                        the_table_fields = p1.split(request.form['table-fields'])
                        my_crud.create_table("127.0.0.1", "root", "xxxxxxxx", request.form['dbname'], request.form['table-name'], the_table_fields)
                    else:
                        return "Can't create table without table name or fields"
    else:
        return "Nothing posted...."

    junk2 = my_crud.list_tables("127.0.0.1", "root", "xxxxxxxx", db_name)
    html1 = "<table>"
    for i in junk2:
        html1 = html1 + "<tr><td>"

        html1 = html1 + '<form action="/table-list" method="post"  style="display: inline;">'
        html1 = html1 + '<input type="hidden" name="dbname" value="' + db_name + '">'
        html1 = html1 + '<input type="hidden" name="table-name" value="' + i[0] + '">'
        html1 = html1 + '<input type="hidden" name="action" value="delete">'
        html1 = html1 + '<input type="image" src="static/delete.png" alt="Submit"></form>'

        html1 = html1 + '<form action="/table-row" method="post"  style="display: inline;">'
        html1 = html1 + '<input type="hidden" name="dbname" value="' + db_name + '">'
        html1 = html1 + '<input type="hidden" name="table-name" value="' + i[0] + '">'
        html1 = html1 + '<input type="hidden" name="action" value="list">'
        html1 = html1 + '<input type="image" src="static/menu.png" alt="Submit"></form>'
        html1 = html1 + i[0] + "</td></tr>"
    html1 = html1 + "</table>"
    return render_template('table-list.html', db_name=db_name, table_list=html1)


@app.route("/table-row", methods=['POST', 'GET'])
def table_row():

    db_name = ""
    if request.method == 'POST':

        if 'dbname' in request.form and 'table-name' in request.form:
            db_name = request.form['dbname']
            # goes up here because we need the row descriptions for the create from
            junk3 = my_crud.describe_table("127.0.0.1", "root", "xxxxxxxx", db_name, request.form['table-name'])
        else:
            return "No DB name or table name set"

        if 'action' in request.form:
            if request.form['action'] == 'create':
                fields = []
                for i in junk3:
                    if i != "ID":
                        fields.append(request.form[i])
                my_crud.insert_data("127.0.0.1", "root", "xxxxxxxx", db_name, request.form['table-name'], fields)
            if request.form['action'] == 'delete':
                if 'row-id' in request.form:
                    my_crud.delete_data("127.0.0.1", "root", "xxxxxxxx", db_name, request.form['table-name'], request.form['row-id'])
                else:
                    return "No row-id"

    else:
        return "Nothing posted...."

    # goes down here so we have updated info after inserting new rows
    junk2 = my_crud.print_all("127.0.0.1", "root", "xxxxxxxx", db_name, request.form['table-name'])

    form1 = '<form action="/table-row" method="post">'
    form1 = form1 + '<input type="hidden" name="action" value="create">'
    form1 = form1 + '<input type="hidden" name="dbname" value="' + db_name + '">'
    form1 = form1 + '<input type="hidden" name="table-name" value="' + request.form['table-name'] + '">'
    for i in junk3:
        if i != "ID":
            form1 = form1 + i + ': <input type="text" name="' + i + '">'
    form1 = form1 + '<input type="image" src="static/new.png" alt="Submit"></form>'

    html1 = "<table>"
    html1 = html1 + "<tr>"
    html1 = html1 + "<th></th>"
    for i in junk3:
        html1 = html1 + "<th>" + str(i) + "</th>"
    html1 = html1 + "</tr>"
    for i in junk2:
        row_id = i[0]

        html1 = html1 + "<tr>"
        html1 = html1 + "<td>"
        html1 = html1 + '<form action="/table-row" method="post"  style="display: inline;">'
        html1 = html1 + '<input type="hidden" name="dbname" value="' + db_name + '">'
        html1 = html1 + '<input type="hidden" name="table-name" value="' + request.form['table-name'] + '">'
        html1 = html1 + '<input type="hidden" name="row-id" value="' + str(row_id) + '">'
        html1 = html1 + '<input type="hidden" name="action" value="delete">'
        html1 = html1 + '<input type="image" src="static/delete.png" alt="Submit"></form>'

        # LAUNCH a New page for editing a row....
        #html1 = html1 + '<form action="/table-row" method="post"  style="display: inline;">'
        #html1 = html1 + '<input type="hidden" name="dbname" value="' + db_name + '">'
        #html1 = html1 + '<input type="hidden" name="table-name" value="' + 'xxxx' + '">'
        #html1 = html1 + '<input type="hidden" name="action" value="list">'
        #html1 = html1 + '<input type="image" src="static/menu.png" alt="Submit"></form>'

        html1 = html1 + "</td>"

        for x in i:
            html1 = html1 + "<td>" + str(x) + "</td>"
        html1 = html1 + "</tr>"
    html1 = html1 + "</table>"
    return render_template('table-row.html', db_name=db_name, table_name=request.form['table-name'], row_list=html1, form1=form1)


@app.route("/row", methods=['POST', 'GET'])
def row():

    db_name = ""
    if request.method == 'POST':

        if 'dbname' in request.form and 'table-name' in request.form:
            db_name = request.form['dbname']
        else:
            return "No DB name or table name set"

        if 'action' in request.form:
            pass

    return render_template('row.html', db_name=db_name, table_name=request.form['table-name'])




if __name__ == "__main__":
    app.run()


















