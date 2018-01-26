## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests, json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    name = StringField('Enter the name of an album:', validators=[Required()])
    rating = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1','choice1'),('2','choice2'), ('3', "choice3")], validators=[Required()])
    submit = SubmitField("Submit")



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

#Part 1
# `http://localhost:5000/artistform` -> `artistform.html`
# `http://localhost:5000/artistinfo` -> `artist_info.html`
# `http://localhost:5000/artistlinks` -> `artist_links.html`
# `http://localhost:5000/specific/song/<artist_name>` -> `specific_artist.html`
@app.route('/artistform', methods = ['POST', 'GET'])
def artistform():
    if request.args.get("Submit") == "None":
        return redirect(url_for('artistinfo', result=request.args.get("Submit")))
    return render_template("artistform.html")

@app.route('/artistinfo', methods = ['GET'])
def artistinfo():
    if request.args.get("artist") is not None and request.args.get("artist") != "":
        artist = request.args.get("artist")
        itunesAPI = "https://itunes.apple.com/search?term=" + artist + "&entity=musicTrack"
        response = requests.get(itunesAPI)
        return render_template("artist_info.html", objects = response.json()["results"])
    return """<h1>No Artist Given.</h1><a href="/artistform"><button>Click Here.</button></a>"""

@app.route('/artistlinks')
def artistlinks():
    return render_template("artist_links.html")

@app.route('/specific/song/<artist_name>')
def specificsong(artist_name):
    itunesAPI = "https://itunes.apple.com/search?term=" + artist_name + "&entity=musicTrack"
    response = requests.get(itunesAPI)
    return render_template("specific_artist.html", results = response.json()["results"])

#Part 2
#Form named AlbumEntryForm with fields:
# Text entry for an album name, whose label should be `Enter the name of an album:`, which should be **required**
# Radio buttons with options: 1,2,3 -- representing how much the user likes the album, whose label should be: `How much do you like this album? (1 low, 3 high)`, which should be **required**
# A submit button
# 2 more routes that should be in a template format (later in part 3) /album_entry and /album_result

@app.route('/album_entry', methods = ['POST', 'GET'])
def albumentry():
    form = AlbumEntryForm()
    return render_template("album_entry.html", form=form)

@app.route('/album_result', methods = ['POST', 'GET'])
def albumresult():
    form = AlbumEntryForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        rating = form.rating.data
        return render_template("album_data.html", name=name, rating=rating)
    return """<h1>No data given.</h1><a href="/album_entry"><button>Click Here.</button></a>"""

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
