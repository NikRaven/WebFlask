from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)  # передаёт сам файл в котором мы всё это делаем
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(
# os.path.abspath(os.path.dirname('pythonProject8')), 'dpd_test.db')
db = SQLAlchemy(app)  # создаём объект на основе класса скьюэл алхимия и передаём туда объект нашего фласка


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # nullable фолс означает что это поле не может бытьь пустым
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # время и дата когда мы добавляем статью

    def __repr__(self):
        return '<Article %r>' % self.id  # выдаём сам объект и его id


@app.route('/')  # создаём главную страничку через декоратор
@app.route('/home')
def index():
    return render_template("index.html")  # "Main Flask page"


@app.route('/about')  # создаём главную страничку через декоратор
def about():
    return render_template("about.html")  # "About Flask page"


@app.route('/posts')  # создаём главную страничку через декоратор
def posts():
    articles = Article.query.order_by(Article.date.desc()).all() #обращаемся к бд, добавляем запись и сортировку по полю даты
    return render_template("posts.html", articles=articles)  # "About Flask page"


@app.route('/posts/<int:id>')  # страничка для детального рассмотрения конкретной статьи
def post_detail(id):
    article = Article.query.get(id)  # получаем определённый объект по его id
    return render_template("post_detail.html", article=article)  # "About Flask page"


@app.route('/posts/<int:id>/delete')  # страничка для удаления конкретной статьи
def post_delete(id):
    article = Article.query.get_or_404(id)  # если не будет найдена запись по id, то будет вызвана ошибка 404

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи возникла ошибка"


@app.route('/posts/<int:id>/update',
           methods=['POST', 'GET'])  # создаём страничку для изменения конкретной статьи
def update_post(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи возникла ошибка"
    else:
        return render_template("update_post.html",article=article)  # для публикации статьи


@app.route('/create-article',
           methods=['POST', 'GET'])  # создаём главную страничку для публикации статьи через декоратор, post & get указываем чтобы получать ответ
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи возникла ошибка"
    else:
        return render_template("create-article.html")  # для публикации статьи


@app.route('/user/<string:name>/<int:id>')  # создаём главную страничку через декоратор
def user(name, id):
    return "User page: " + name + " -- " + str(id)


if __name__ == "__main__":
    app.run(
        debug=True)  # пока стоит значение True, мы будем видеть все ошибки на сайте, при перебросе на сервер следует заменить на False
