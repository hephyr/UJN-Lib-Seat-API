#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Required

from GetSeat import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

times = [
            ('7', '7:00'),
            ('8', '8:00'),
            ('9', '9:00'),
            ('10', '10:00'),
            ('11', '11:00'),
            ('12', '12:00'),
            ('13', '13:00'),
            ('14', '14:00'),
            ('15', '15:00'),
            ('16', '16:00'),
            ('17', '17:00'),
            ('18', '18:00'),
            ('19', '19:00'),
            ('20', '20:00'),
            ('21', '21:00'),
            ('22', '22:00')
]


class SeatForm(Form):
    p = PersonLib()
    room_id = SelectField(u"房间", coerce=str, choices=p.getBuildingsList())
    seat_num = StringField(u'座位号', validators=[Required()])
    start_time = SelectField(u"开始时间", choices=times[:-1])
    end_time = SelectField(u"结束时间", choices=times[1:])
    dates = []
    for i, value in enumerate(p.dates):
        dates.append((str(i+1), value))
    resDate = SelectField(u"日期", choices=dates)
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    text = u''
    form = SeatForm()
    if form.validate_on_submit():
        room_id = form.room_id.data
        seat_num = form.seat_num.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        resDate = form.resDate.data
        text = hackBook(room_id, seat_num, start_time, end_time, resDate)
        text = unicode(text, "utf-8")
    return render_template('index.html', form=form, text=text)


if __name__ == '__main__':
    manager.run()
