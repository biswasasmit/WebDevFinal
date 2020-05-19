## Main routes

from flask import render_template, redirect, url_for, Response, Blueprint, flash
from flask_mail import Message
from flask_login import current_user
from ..forms import SearchForm, InviteFriendForm
from .. import client, mail

main = Blueprint("main", __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('main.query_results', query=form.search_query.data))

    return render_template('index.html', form=form)

@main.route('/search-results/<query>', methods=['GET'])
def query_results(query):
    results = client.search(query)
    print(results)

    if type(results) == dict:
        return render_template('query.html', error_msg=results['Error'])
    
    return render_template('query.html', results=results)

@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@main.route('/invite', methods=['POST', 'GET'])
def invite():
    invite_form = InviteFriendForm()
    invite_form.subject.data = f'Hello from {current_user.username}!'
    if invite_form.validate_on_submit():
        msg = Message(f'Hello from {current_user.username}!', sender = ('GoodPlays', 'goodplays2020@gmail.com'), recipients = [invite_form.email.data])
        msg.body = invite_form.body.data
        mail.send(msg)
        flash("Sent email!")
        return redirect(url_for('main.invite'))
    
    return render_template("invite.html", invite_form=invite_form)