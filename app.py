from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate=Migrate(app,db)

class student(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(),nullable=True)
	completed=db.Column(db.Boolean,nullable=False)

	def __repr__(self):
		return f'<{self.id} {self.name}>'

#db.create_all()

@app.route('/create', methods=['POST'])
def create_todo():
	na=request.form['disc']
	todo=student(name=na,completed=False)
	db.session.add(todo)
	db.session.commit()
	return redirect(url_for('index'))


@app.route('/create/<id>/set-completed', methods=['POST'])
def set_complete_student(id):
	try:
		check=request.get_json()['completed']
		print('completed', check)
		st=student.query.get(id)
		st.completed=check
		db.session.commit()
	except:
		db.session.rollback()
	finally:
		db.session.close()
	return redirect(url_for('index'))
@app.route('/create/<id>',methods=['DELETE'])
def del_student(id):
	try:
		st=student.query.get(id)
		db.session.delete(st)
		db.session.commit()
	except:
		db.session.rollback()
	finally:
		db.session.close()

	#return redirect(url_for('index'))
	return jsonify({
		'succuss':True
		})

@app.route('/')
def index():
	names=student.query.order_by('id').all()
	return render_template('index.html',names=names)

if __name__==('__main__'):
	app.run(debug=True)


# @app.route('/login', methods=['POST'])
# # def app_login():
# 	if request.method=='POST':
# 		user=request.form.get('username')
# 		password=request.form.get('password')
# 		return render_template('login')
# 	