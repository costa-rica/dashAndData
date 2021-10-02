from dashAndData import db
from datetime import datetime, date
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask import current_app
# from flask_login import UserMixin

# from flask_script import Manager




# @login_manager.user_loader
# def load_user(user_id):
    # return User.query.get(int(user_id))
    

# class User(db.Model, UserMixin):
    # id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(150), unique=True, nullable=False)
    # image_file = db.Column(db.String(100),nullable=False, default='default.jpg')
    # password = db.Column(db.String(100), nullable=False)
    # timeStamp = db.Column(db.DateTime, default=datetime.now)
    # permission = db.Column(db.Text)
    # theme = db.Column(db.Text)
    # posts = db.relationship('Post', backref='author', lazy=True)
    # track_inv = db.relationship('Tracking_inv', backref='updator_inv', lazy=True)
    # track_re = db.relationship('Tracking_re', backref='updator_re', lazy=True)
    # query_string_inv = db.relationship('Saved_queries_inv', backref='query_creator_inv', lazy=True)
    # query_string_re = db.relationship('Saved_queries_re', backref='query_creator_re', lazy=True)

    # def get_reset_token(self, expires_sec=1800):
        # s=Serializer(current_app.config['SECRET_KEY'], expires_sec)
        # return s.dumps({'user_id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_reset_token(token):
        # s=Serializer(current_app.config['SECRET_KEY'])
        # try:
            # user_id = s.loads(token)['user_id']
        # except:
            # return None
        # return User.query.get(user_id)

    # def __repr__(self):
        # return f"User('{self.id}','{self.email}','{self.permission}')"

# class Post(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # title= db.Column(db.String(100), nullable=False)
    # date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # content = db.Column(db.Text)
    # screenshot = db.Column(db.String(100))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # def __repr__(self):
        # return f"Post('{self.title}','{self.date_posted}')"



#From folioApp.models.py
class Industrynames(db.Model):
	# id = db.Column(db.Integer, primary_key=True)
	series_id = db.Column(db.String(200), primary_key=True)
	industry_code = db.Column(db.String(100))
	product_code = db.Column(db.String(100))
	seasonal = db.Column(db.String(10))
	base_date = db.Column(db.String(10))
	series_title = db.Column(db.String(200))
	footnote_codes = db.Column(db.String(10))
	begin_year = db.Column(db.Integer)
	begin_period = db.Column(db.String(3))
	end_year = db.Column(db.Integer)
	end_period = db.Column(db.String(3))
	values = db.relationship('Industryvalues', backref='values', lazy=True)
    
    
	def __repr__(self):
		return f"Industrynames({self.series_id},{self.series_title})"

class Industryvalues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.String(200), db.ForeignKey('industrynames.series_id'))
    # series_id = db.Column(db.String(200), db.ForeignKey('industrynames.series_id'))
    year = db.Column(db.Integer)
    period = db.Column(db.String(3))
    value = db.Column(db.Float)
    footnote_codes = db.Column(db.String(10))
    # namesId = db.Column(db.Integer, db.ForeignKey('industrynames.id'))

    def __repr__(self):
        return f"Industryvalues({self.id},{self.series_id},{self.year},{self.period},{self.value})"


class Commoditynames(db.Model):
	series_id = db.Column(db.String(200), primary_key=True)
	group_code = db.Column(db.String(100))
	item_code = db.Column(db.String(100))
	seasonal = db.Column(db.String(10))
	base_date = db.Column(db.String(10))
	series_title = db.Column(db.String(200))
	footnote_codes = db.Column(db.String(10))
	begin_year = db.Column(db.Integer)
	begin_period = db.Column(db.String(3))
	end_year = db.Column(db.Integer)
	end_period = db.Column(db.String(3))
	values = db.relationship('Commodityvalues', backref='values', lazy=True)
    
    
	def __repr__(self):
		return f"Commoditynames({self.series_id},{self.series_title})"

class Commodityvalues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.String(200), db.ForeignKey('commoditynames.series_id'))
    year = db.Column(db.Integer)
    period = db.Column(db.String(3))
    value = db.Column(db.Float)
    footnote_codes = db.Column(db.String(10))


    def __repr__(self):
        return f"Commodityvalues({self.id},{self.series_id},{self.year},{self.period},{self.value})"