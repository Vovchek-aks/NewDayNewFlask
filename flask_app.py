from flask import Flask, redirect, render_template, request, abort, make_response, jsonify
from data import db_session, get_jobs_api, get_one_job_api, del_job_api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime as dt
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.job_add import AddJobForm
from data.users import User
from data.job import Job

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()

    return render_template('index.html', title='Домашняя страница', jobs=jobs,
                           db_sess=db_sess,
                           User=User)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            modified_date=dt.date.today()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        if form.start_of_piatiletka.data == form.end_of_piatiletka.data:
            return render_template('add_job.html', title='Да здравствует тов.Сталин!', form=form,
                                   form_items=[form.__dict__['_fields'][i] for i in
                                               list(form.__dict__['_fields'])[:-2]],
                                   message='Дурак?')
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == form.politryk_id.data).first():
            return render_template('add_job.html', title='Да здравствует тов.Сталин!', form=form,
                                   form_items=[form.__dict__['_fields'][i] for i in
                                               list(form.__dict__['_fields'])[:-2]],
                                   message='Такого палитрука нет. Вы деверсант?')
        job = Job(
            politryk_id=form.politryk_id.data,
            creater_id=current_user.id,
            name=form.name.data,
            plan=form.plan.data,
            ids_tovarishei=form.ids_tovarishei.data,
            start_of_piatiletka=form.start_of_piatiletka.data,
            end_of_piatiletka=form.end_of_piatiletka.data,
            result_of_plan=form.result_of_plan.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Да здравствует тов.Сталин!', form=form,
                           form_items=[form.__dict__['_fields'][i] for i in list(form.__dict__['_fields'])[:-2]])


@app.route('/edit_job/<job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = AddJobForm()

    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Job).filter(Job.id == job_id).first()
        print(123)
        if job:
            form.name.data = job.name
            form.politryk_id.data = job.politryk_id
            form.ids_tovarishei.data = job.ids_tovarishei
            form.plan.data = job.plan
            form.ids_tovarishei.data = job.ids_tovarishei
            form.start_of_piatiletka.data = job.start_of_piatiletka
            form.end_of_piatiletka.data = job.end_of_piatiletka
            form.result_of_plan.data = job.result_of_plan
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Job).filter(Job.id == job_id).first()
        if job:
            job.name = form.name.data
            job.politryk_id = form.politryk_id.data
            job.ids_tovarishei = form.ids_tovarishei.data
            job.plan = form.plan.data
            job.ids_tovarishei = form.ids_tovarishei.data
            job.start_of_piatiletka = form.start_of_piatiletka.data
            job.end_of_piatiletka = form.end_of_piatiletka.data
            job.result_of_plan = form.result_of_plan.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)

    return render_template('add_job.html', title='Да здравствует тов.Сталин! снова...', form=form,
                           form_items=[form.__dict__['_fields'][i] for i in list(form.__dict__['_fields'])[:-2]])


@app.route('/job_delete/<int:job_id>', methods=['GET', 'POST'])
@login_required
def job_delete(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == job_id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(get_jobs_api.blueprint)
    app.register_blueprint(get_one_job_api.blueprint)
    app.register_blueprint(del_job_api.blueprint)
    app.run(debug=True)


if __name__ == '__main__':
    main()
