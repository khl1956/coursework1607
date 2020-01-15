from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
import json
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Text, CheckConstraint, Sequence, Float, \
    UniqueConstraint
from sqlalchemy.orm import relationship
import datetime
from forms.text_data_form import CreateTextData, EditTextData
from forms.command_list_form import CreateCommandList, EditCommandList
from forms.voice_pattern_form import CreateVoicePattern, EditVoicePattern
from forms.command_form import CreateCommand, EditCommand
from forms.searchform import CreateQuery
import plotly
import plotly.graph_objs as go
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from neupy import algorithms

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'prod'


app.debug = False
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://fsbaqfsajqwozv:caef19e50620d092450249249d54f552f586874de10ce1e339a5b24f55f508df@ec2-174-129-33-75.compute-1.amazonaws.com:5432/d90f5l3d6t81u3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ormVoice_Pattern(db.Model):
    __tablename__ = 'voice_pattern'
    id = Column(Integer, Sequence('users_user_id_seq', start=1, increment=1), primary_key=True)
    voice_body = Column(String(30), UniqueConstraint(name='users_voice_body_key'), nullable=False)
    voice_emotion_logic_accent = Column(String(30))
    voice_pronunciation_date = Column(DateTime, default=datetime.datetime.now())
    voicePatternRelationShip = relationship("ormText_Data", back_populates="voice_Pattern_Relation_Ship")


class ormText_Data(db.Model):
    __tablename__ = 'text_data'
    id = Column(Integer, Sequence('text_data_id_seq', start=1, increment=1), primary_key=True)
    text_body = Column(Text)
    text_pronunciation_time = Column(DateTime, default=datetime.datetime.now())
    text_id = Column(Integer, CheckConstraint('text_id >= 0'), nullable=False, default=0)
    voice_Pattern_Relation_Ship = relationship("ormVoice_Pattern", back_populates="voicePatternRelationShip")
    textDataRelationShip = relationship("ormCommand_List", back_populates="text_Data_Relation_Ship")


class ormCommand_List(db.Model):
    __tablename__ = 'command_list'
    id = Column(Integer, Sequence('command_list_id_seq', start=1, increment=1), primary_key=True)
    command_body_text = Column(String(30), nullable=False)
    сommand_group_data = Column(Text)
    #created = Column(DateTime, default=datetime.datetime.now())
    countofcommands = Column(Integer, CheckConstraint('countofcommands >= 0'), nullable=False, default=0)
    #reposytoty_id = Column(Integer, ForeignKey('reposytoty.id'))
    text_Data_Relation_Ship = relationship("ormText_Data", back_populates="textDataRelationShip")
    commandRelationShip = relationship("ormCommand", back_populates="command_Relation_Ship")


class ormCommand(db.Model):
    __tablename__ = 'command'
    id = Column(Integer, Sequence('files_id_seq', start=1, increment=1), primary_key=True)
    name = Column(String(30), nullable=False)
    command_body = Column(Text)
    expansion = Column(String(10), nullable=False)
    versions = Column(String(30), nullable=False, default='1.0')
    created = Column(DateTime, default=datetime.datetime.now())
    rating = Column(Float)
    belongs_to_id_fkey = Column(Integer, ForeignKey('voice_pattern.id'))
    command_Relation_Ship = relationship("ormCommand_List", back_populates="commandRelationShip")


@app.route('/')
def hello_world():
    text = ""
    return render_template('index.html', action="/")


@app.route('/all/voice_pattern')
def all_voice_pattern():
    name = "voice_pattern"
    voice_pattern_db = db.session.query(ormVoice_Pattern).all()
    voice_pattern = []
    for row in voice_pattern_db:
        voice_pattern.append({"id": row.id, "voice_body": row.voice_body,
                     "voice_emotion_logic_accent": row.voice_emotion_logic_accent, "voice_pronunciation_date": row.voice_pronunciation_date})
    return render_template('allVoice_Pattern.html', name=name, voice_patterns=voice_pattern, action="/all/voice_pattern")


@app.route('/all/text_data')
def all_text_data():
    name = "text_data"
    text_data_db = db.session.query(ormText_Data).all()
    text_data = []
    for row in text_data_db:
        text_data.append({"id": row.id, "text_body": row.text_body, "text_pronunciation_time": row.text_pronunciation_time,
                           "text_id": row.text_id})
    return render_template('allText_Data.html', name=name, text_data=text_data, action="/all/text_data")


@app.route('/all/command_list')
def all_command_list():
    name = "command_list"
    command_list_db = db.session.query(ormCommand_List).all()
    command_list = []
    for row in command_list_db:
        command_list.append({"id": row.id, "command_body_text": row.command_body_text, "сommand_group_data": row.сommand_group_data})
    return render_template('allCommand_List.html', name=name, command_list=command_list, action="/all/command_list")


@app.route('/all/command')
def all_command():
    name = "command"
    command_db = db.session.query(ormCommand).all()
    command = []
    for row in command_db:
        command.append({"id": row.id, "command_body": row.command_body, "belongs_to_id_fkey": row.belongs_to_id_fkey})
    return render_template('allCommand.html', name=name, command=command, action="/all/command")


@app.route('/create/voice_pattern', methods=['GET', 'POST'])
def create_voice_pattern():
    form = CreateVoicePattern()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_voice_pattern.html', form=form, form_name="New voice_pattern", action="create/voice_pattern")
        else:

            ids = db.session.query(ormVoice_Pattern).all()
            check = True
            for row in ids:
                if row.voice_body == form.voice_body.data:
                    check = False

            new_var = ormVoice_Pattern(

                voice_body=form.voice_body.data,
                voice_emotion_logic_accent=form.voice_emotion_logic_accent.data

            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_voice_pattern'))
            else:
                form.voice_body.errors = "this voice pattern already exists"

    return render_template('create_voice_pattern.html', form=form, form_name="New voice pattern", action="create/voice_pattern")


@app.route('/create/text_data', methods=['GET', 'POST'])
def create_text_data():
    form = CreateTextData()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_text_data.html', form=form, form_name="New text data",
                                   action="create/text_data")
        else:

            ids = db.session.query(ormVoice_Pattern).all()
            check = False
            #for row in ids:
             #   if row.id == form.id.data:
              #      check = True

            new_var = ormText_Data(

                text_body=form.text_body.data,
                text_id=form.text_id.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_text_data'))

    return render_template('create_text_data.html', form=form, form_name="New text data", action="create/text_data")


@app.route('/create/command_list', methods=['GET', 'POST'])
def create_command_list():
    form = CreateCommandList()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_command_list.html', form=form, form_name="New command_list", action="create/command_list")
        else:

            ids = db.session.query(ormText_Data).all()
            check = False
            #for row in ids:
             #   if row.id == form.reposytoty_id.data:
              #      check = True

            new_var = ormCommand_List(

                command_body_text=form.command_body_text.data,
                сommand_group_data=form.сommand_group_data.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_command_list'))

    return render_template('create_command_list.html', form=form, form_name="New command list", action="create/command_list")


@app.route('/create/command', methods=['GET', 'POST'])
def create_command():
    form = CreateCommand()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_command.html', form=form, form_name="New command", action="create/command")
        else:

            ids = db.session.query(ormCommand_List.all()
            check = False
            for row in ids:
                if row.id == form.belongs_to_id_fkey.data:
                    check = True

            new_var = ormCommand(

                command_body_text=form.command_body_text.data,
                belongs_to_id_fkey=form.belongs_to_id_fkey.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_command'))

    return render_template('create_command.html', form=form, form_name="New command", action="create/command")


@app.route('/delete/voice_pattern', methods=['GET'])
def delete_voice_pattern():
    id = request.args.get('id')

    result = db.session.query(ormVoice_Pattern).filter(ormVoice_Pattern.id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_voice_pattern'))


@app.route('/delete/text_data', methods=['GET'])
def delete_text_data():
    id = request.args.get('id')

    result = db.session.query(ormText_Data).filter(ormText_Data.id == id).one()

    # db.session.delete(result)
    #
    # result = db.session.query(ormCommand_List).filter(ormCommand_List.reposytoty_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_text_data'))


@app.route('/delete/command_list', methods=['GET'])
def delete_command_list():
    id = request.args.get('id')

    result = db.session.query(ormCommand_List).filter(ormCommand_List.id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_command_list'))


@app.route('/delete/command', methods=['GET'])
def delete_command():
    id = request.args.get('id')

    result = db.session.query(ormCommand).filter(ormCommand.id == id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_command'))


@app.route('/edit/voice_pattern', methods=['GET', 'POST'])
def edit_voice_pattern():
    form = EditVoicePattern()
    id = request.args.get('id')
    if request.method == 'GET':

        users = db.session.query(ormVoice_Pattern).filter(ormVoice_Pattern.id == id).one()

        form.voice_body.data = users.voice_body
        #form.password.data = users.password
        #form.email.data = users.email
        form.voice_emotion_logic_accent.data = users.voice_emotion_logic_accent
        #form.firstname.data = users.firstname

        return render_template('edit_voice_pattern.html', form=form, form_name="Edit voice pattern",
                               action="edit/voice_pattern?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_voice_pattern.html', form=form, form_name="Edit voice pattern", action="edit/voice_pattern?id=" + id)
        else:

            # find voice pattern
            var = db.session.query(ormVoice_Pattern).filter(ormVoice_Pattern.id == id).one()
            print(var)

            # update fields from form data

            var.voice_body = form.voice_body.data
            #var.password = form.password.data
            #var.email = form.email.data
            var.voice_emotion_logic_accent = form.voice_emotion_logic_accent.data
            #var.firstname = form.firstname.data
            db.session.commit()

            return redirect(url_for('all_voice_pattern'))


@app.route('/edit/text_data', methods=['GET', 'POST'])
def edit_text_data():
    form = EditTextData()
    id = request.args.get('id')
    if request.method == 'GET':

        text_data = db.session.query(ormText_Data).filter(ormText_Data.id == id).one()

        #form.name.data = text_data.name
        form.text_body.data = text_data.text_body
        form.text_id.data = text_data.text_id

        return render_template('edit_text_data.html', form=form, form_name="Edit text data",
                               action="edit/text_data?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_text_data.html', form=form, form_name="Edit text data",
                                   action="edit/text_data?id=" + id)
        else:

            # find user
            var = db.session.query(ormText_Data).filter(ormText_Data.id == id).one()
            print(var)

            # update fields from form data

            #var.name = form.name.data
            var.text_body = form.text_body.data
            var.text_id = form.text_id.data
            db.session.commit()

            return redirect(url_for('all_text_data'))


@app.route('/edit/command_list', methods=['GET', 'POST'])
def edit_command_list():
    form = EditCommandList()
    id = request.args.get('id')
    if request.method == 'GET':

        command_list = db.session.query(ormCommand_List).filter(ormCommand_List.id == id).one()

        form.command_body_text.data = command_list.command_body_text
        form.сommand_group_data.data = command_list.сommand_group_data
        form.countofcommands.data = command_list.countofcommands

        return render_template('edit_command_list.html', form=form, form_name="Edit command_list",
                               action="edit/command_list?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_command_list.html', form=form, form_name="Edit command_list", action="edit/command_list?id=" + id)
        else:

            # find user
            var = db.session.query(ormCommand_List).filter(ormCommand_List.id == id).one()
            print(var)

            # update fields from form data

            var.command_body_text = form.command_body_text.data
            var.сommand_group_data = form.сommand_group_data.data
            var.countofcommands = form.countofcommands.data
            db.session.commit()

            return redirect(url_for('all_command_list'))


@app.route('/edit/command', methods=['GET', 'POST'])
def edit_command():
    form = EditCommand()
    id = request.args.get('id')
    if request.method == 'GET':

        command = db.session.query(ormCommand).filter(ormCommand.id == id).one()

        #form.name.data = command.name
        form.command_body.data = command.command_body
        #form.versions.data = command.versions
        #form.rating.data = command.rating

        return render_template('edit_command.html', form=form, form_name="Edit command",
                               action="edit/command?id=" + id)


    else:

        if form.validate() == False:
            return render_template('edit_command.html', form=form, form_name="Edit command", action="edit/command?id=" + id)
        else:

            # find user
            var = db.session.query(ormCommand).filter(ormCommand.id == id).one()
            print(var)

            # update fields from form data

            #var.name = form.name.data
            var.command_body = form.command_body.data
            #var.versions = form.versions.data
            #var.rating = form.rating.data
            db.session.commit()

            return redirect(url_for('all_command'))


@app.route('/dashboard')
def dashboard():
    query1 = (
        db.session.query(
            func.count(),
            ormCommand.expansion
        ).group_by(ormCommand.expansion)
    ).all()

    query = (
        db.session.query(
            func.count(ormVoice_Pattern.id),
            ormVoice_Pattern.created
        ).group_by(ormVoice_Pattern.created)
    ).all()

    dates, counts = zip(*query)
    bar = go.Bar(
        x=counts,
        y=dates
    )

    skills, user_count = zip(*query1)
    pie = go.Pie(
        labels=user_count,
        values=skills
    )
    print(dates, counts)
    print(skills, user_count)

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/clasteresation', methods=['GET', 'POST'])
def claster():
    df = pd.DataFrame()

    for name, expansion in db.session.query(ormCommand_List.name, ormCommand.expansion).join(ormCommand,
                                                                                      ormCommand_List.id == ormCommand.command_list_id):
        print(name, expansion)
        df = df.append({"name": name, "expansion": expansion}, ignore_index=True)

    X = pd.get_dummies(data=df)
    print(X)
    count_clasters = len(df['expansion'].unique())
    print(count_clasters)
    kmeans = KMeans(n_clusters=count_clasters, random_state=0).fit(X)
    # print(kmeans)
    count_columns = len(X.columns)
    test_list = [0] * count_columns
    test_list[0] = 1
    test_list[-2] = 1
    print(test_list)
    # print(kmeans.labels_)
    print(kmeans.predict(np.array([test_list])))

    query1 = (
        db.session.query(
            func.count(),
            ormCommand.expansion
        ).group_by(ormCommand.expansion)
    ).all()
    skills, user_count = zip(*query1)
    pie = go.Pie(
        labels=user_count,
        values=skills
    )
    data = {
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('clasteresation.html', row=kmeans.predict(np.array([test_list]))[0],
                           count_claster=count_clasters, graphsJSON=graphsJSON)


@app.route('/regretion', methods=['GET', 'POST'])
def correlation():
    df = pd.DataFrame()
    for count_proj, count_files in db.session.query(ormText_Data.countofcommand_lists, ormCommand_List.countofcommands).join(
            ormText_Data,
            ormText_Data.id == ormCommand_List.reposytoty_id):
        print(count_proj, count_files)
        df = df.append({"count_proj": float(count_proj), "count_files": float(count_files)}, ignore_index=True)
    db.session.close()
    scaler = StandardScaler()
    scaler.fit(df[["count_proj"]])
    train_X = scaler.transform(df[["count_proj"]])
    # print(train_X, df[["count_files"]])
    reg = LinearRegression().fit(train_X, df[["count_files"]])

    test_array = [[3]]
    test = scaler.transform(test_array)
    result = reg.predict(test)

    query1 = db.session.query(ormText_Data.countofcommand_lists, ormCommand_List.countofcommands).join(
            ormText_Data, ormText_Data.id == ormCommand_List.reposytoty_id).all()
    count_pr, count_fl = zip(*query1)
    scatter = go.Scatter(
        x=count_pr,
        y=count_fl,
        mode = 'markers',
        marker_color='rgba(255, 0, 0, 100)',
        name = "data"
    )
    x_line = np.linspace(0, 10)
    y_line = x_line * reg.coef_[0, 0] + reg.intercept_[0]
    line = go.Scatter(
        x=x_line,
        y=y_line,
        mode = 'lines',
        marker_color='rgba(0, 0, 255, 100)',
        name = "regretion"
    )
    data = [scatter, line]
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('regretion.html', row=int(round(result[0, 0])), test_data=test_array[0][0], coef=reg.coef_[0],
                           coef1=reg.intercept_, graphsJSON = graphsJSON)

@app.route('/clasification', methods=['GET', 'POST'])
def clasification():
    df = pd.DataFrame()
    for file_text, rating in db.session.query(ormCommand.file_text, ormCommand.rating):
        print(file_text, rating)
        df = df.append({"file_name": file_text, "rating": float(rating)}, ignore_index=True)
    # db.session.close()

    df['count_symbols'] = df['file_name'].apply(len)
    df.loc[df['rating'] < 0.33, 'quality'] = 0
    df.loc[df['rating'] >= 0.33, 'quality'] = 1
    print(df)
    pnn = algorithms.PNN(std=10, verbose=False)
    pnn.train(df['count_symbols'], df['quality'])

    test_data = 'ewij weioh uia guu aweg'
    t_test_data = len(test_data)
    y_predicted = pnn.predict([t_test_data])
    result = "Ні"
    if y_predicted - 1 < 0.0000000000001:
        result = "Так"

    return render_template('clasification.html', y_predicted=result, test_data=test_data)


list_event = []


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = CreateQuery()
    if request.method == 'POST':
        if not form.validate():

            return render_template('search.html', form=form, form_name="Search", action="search")
        else:
            list_event.clear()
            for id, name, Expansion in db.session.query(ormCommand.id, ormCommand.name, ormCommand.expansion
                                                        ):
                if name == form.nameOfProject.data and Expansion == form.Expansion.data:
                    list_event.append(id)

            return redirect(url_for('searchList'))

    return render_template('search.html', form=form, form_name="Search", action="search")

@app.route('/search/result')
def searchList():
    res = []
    try:
        for i in list_event:
            version,rating = db.session \
                .query(ormCommand.versions, ormCommand.rating).filter(ormCommand.id == i).one()
            res.append(
                {"version": version, "rating": rating})
    except:
        print("don't data")
    print(list_event)

    return render_template('search_list_event.html', name="result", results=res, action="/search/result")
if __name__ == '__main__':
    app.run()
