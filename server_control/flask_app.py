from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect

from server_control.objects import password_commands
from server_control.objects.docker_commands import *
from server_control.objects.idrac_commands import *
from server_control.objects.mongo_commands import *
from flask import flash
from datetime import timedelta
import time

app = Flask(__name__)
app._static_folder = 'static/'
app.secret_key = flask_secret_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
service = DockerApi('docker')
server = IdracApi()
mongo = MongoApi('mongo')


@app.route("/")
def homepage():
    if not session.get("logged_in?"):
        return redirect('/login')
    else:
        return redirect('/status')


@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "POST":
        un_check = request.form['un']
        pw_check = request.form['pw']
        if password_commands.check_plex_un_pw(username=un_check, password=pw_check):
            session["logged_in?"] = True
            flash('Successfully logged in!')
            return redirect("/status")
        else:
            flash('Incorrect username, or password')
            return render_template('login.html')
    return render_template('login.html')


@app.route("/status")
def status():
    # TODO fix docker integration
    if not session.get("logged_in?"):
        return redirect('/login')
    else:
        server_status = server.retrieve_idrac_data()
        if server_status is not "on":
            container_status = {
                "plex": "exited",
                "minecraft": "exited"
            }
        else:
            container_status = service.fake_container_status()
        return render_template('status.html', container_status=container_status, server_status=server_status)


@app.route("/service", methods=["post"])
def start_service():
    if not session.get("logged_in?"):
        return redirect('/login')
    else:
        server_action_dict = request.form
        for server_name in server_action_dict:
            action = server_action_dict[server_name]
            if action == 'start':
                service.start_server(server_name)
            elif action == 'stop':
                service.stop_server(server_name)
        server_status = server.retrieve_idrac_data()
        if server_status is not "on":
            container_status = {
                "plex": "exited",
                "minecraft": "exited"
            }
        else:
            container_status = service.fake_container_status()
        return render_template('status.html', container_status=container_status, server_status=server_status)


@app.route("/server", methods=["post"])
def start_server():
    if not session.get("logged_in?"):
        return redirect('/login')
    else:
        server_action = request.form['server']
        if server_action == 'start':
            server.turn_on()
        elif server_action == 'stop':
            server.turn_off()
            time.sleep(2)
        server_status = server.retrieve_idrac_data()
        if server_status is not "on":
            container_status = {
                "plex": "exited",
                "minecraft": "exited"
            }
        else:
            container_status = service.fake_container_status()
        return render_template('status.html', container_status=container_status, server_status=server_status)


@app.route("/logout", methods=["post", "get"])
def logout():
    session['logged_in?'] = False
    return redirect('/')


if __name__ == '__main__':
    app.run()
