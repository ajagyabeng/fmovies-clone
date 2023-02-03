from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///paginate.db"

db = SQLAlchemy(app)


class Thread(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))


with app.app_context():
    db.create_all()


# @app.route("/")
# def add():
#     threads = Thread.query.paginate()
#     print(threads.page)  # shows the current page
#     print(threads.next_num)  # returns the actual number of next page
#     print(threads.prev_num)  # returns the actual number of previous page
#     print(threads.pages)  # shows the total number of pages
#     print(threads.has_next)  # returns True if there is a next page
#     print(threads.has_prev)  # returns True if there is a previous page
#     # print(threads.items)  # returns the actual items in the object
#     # print(threads.next)  # returns the pagination object for the next page
#     # print(threads.prev)  # returns the pagination object for the previous page
#     print(threads.per_page)  # shows the number of items per page
#     print(threads.total)  # shows the total number of items in the query
#     return "Done"

# @app.route("/")
# def show_pagination():
#     threads = Thread.query.paginate(per_page=15, page=4)
#     print(threads.page)
#     print(threads.next_num)
#     print(threads.items)
#     return "Done"


# @app.route("/")
# def show_pagination():
#     threads = Thread.query.paginate(per_page=15, page=4)
#     all_pages = threads.iter_pages()
#     for i in all_pages:
#         print(i)
#     return "Done"

@app.route("/thread/<int:page_num>")
def thread(page_num):
    """
    takes page_num to paginate the items displayed per page
    :param page_num:
    :return:
    """
    threads = Thread.query.paginate(per_page=5, page=page_num, error_out=True)  # error_out decides to display an error page or not
    return render_template("paginate.html", threads=threads)
