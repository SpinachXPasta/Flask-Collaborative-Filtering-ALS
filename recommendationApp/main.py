from flask import Blueprint, render_template,redirect,request
from flask_login import login_required, current_user
from models import User,Artist,Likes
from startup import db
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from sqlalchemy import tablesample, func, select
from sqlalchemy.orm import aliased
from sqlalchemy import create_engine
from ALS import genRecomendation
from tqdm import tqdm

main = Blueprint('main', __name__)
engine = create_engine('sqlite:///Main.db')


@main.route('/')
def index():
    artquery = Artist.query.all()
    print ("\n\n Entries", len(artquery))
    music = pd.read_csv("music.csv")
    if len(artquery) < len(music):
        for m in tqdm(music.values):
            try:
                #print ("\n\n\n New com,m,it",m)
                new_artist = Artist(id = int(m[0]), name = str(m[1]))
                db.session.add(new_artist)
                db.session.commit()
            except:
                pass
        print ("\n\n Commted artists to DB")
    else:
        print ("\n\n Music Database is ready")

    user = User.query.filter_by(email="admin_31@app.io").first()
    if user == None:
        new_user = User(email="admin_31@app.io", name="admin", password=generate_password_hash("2211", method='sha256'))
        db.session.add(new_user)
        db.session.commit()
    return render_template('index.html')

def getRandom(Table):
    sql_ = select([  Table     ]).order_by(func.random()).limit(10)
    q1 = engine.execute(sql_)
    data = [(i[0],i[1]) for i in q1]
    return data


@main.route('/profile')
@login_required
def profile():
    data = getRandom(Artist)
    return render_template('profile.html', name=current_user.name, l1 = data)

@main.route('/save',methods=["POST"])
@login_required
def save():
    s_id = request.form.get("songid")
    musc = request.form.get("songname")
    new_entry = Likes(song_id=int(s_id),artist = musc ,user_email = current_user.email )
    db.session.add(new_entry)
    db.session.commit()
    try:
        querx = request.form.get("red")
        print ("((((())))) \n\n\n", querx)
        if int(querx) == 1:
            return redirect('/myLikes')
    except:
        return redirect('/profile')
    return redirect('/profile')

@main.route('/myLikes',methods=["GET","POST"])
@login_required
def myLikes():
    new_save = "blank"
    try:
        temp = request.form.get("genRec")
        if temp == 'Gen0':
            likes_0 = select([Likes]).where(Likes.user_email == current_user.email)
            tempdf = pd.read_sql(likes_0,'sqlite:///Main.db')
            tdf = tempdf.copy()
            tdf = tdf.drop(columns = ['pm','song_id'])
            tdf['c'] = 1
            tdf = tdf.groupby(['user_email','artist']).sum().reset_index()
            tdf.columns = ['user','artist','plays']
            rec = genRecomendation(tdf)
            rec['red'] = 1
            new_save = list(rec[['artist','song_id','red']].values)
    except:
        pass
    likes = [(i.artist,i.song_id) for i in Likes.query.filter_by(user_email = current_user.email )]
    return render_template('myLikes.html', likes = likes, new_s = new_save)



@main.route('/admin')
@login_required
def admin():
    Q1 = User.query.all()
    return render_template('admin.html', send = Q1)

@main.route('/delete',methods=["POST"])
def delete():
    email = request.form.get("email")
    if email != 'admin_31@app.io':
        Query = User.query.filter_by(email = email).first()
        db.session.delete(Query)
        db.session.commit()
        k = User.query.all()
        return redirect('/admin')
    return redirect('/admin')

@main.route('/delete_song',methods=["POST"])
@login_required
def delete_song():
    email = current_user.email
    todel = request.form.get("sid_del")
    Query = Likes.query.filter_by(user_email = email, song_id = todel).first()
    db.session.delete(Query)
    db.session.commit()
    k = User.query.all()
    return redirect('/myLikes')
