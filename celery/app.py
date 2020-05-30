from celery import chain
from celery import group

from tasks import add
from factory import create_app


app = create_app()


@app.route("/")
def index():
    add.delay(1, 2)
    return "simple"


@app.route("/c")
def chained():
    chain(add.s(1, 2) | add.s(1) | add.s(2))()
    return "chained"


@app.route("/g")
def grouped():
    # this will run in concurrent according to celery concurrency config
    group(add.s(i, i) for i in xrange(10))()
    return "grouped"


if __name__ == "__main__":
    app.run()
