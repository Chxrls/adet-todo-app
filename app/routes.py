from flask import render_template, request, redirect, flash, url_for
from app import app, db
from app.models import Entry

@app.route('/')
@app.route('/index')
def index():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    form = request.form
    title = form.get('title')
    description = form.get('description')
    if title and description:
        entry = Entry(title=title, description=description)
        db.session.add(entry)
        db.session.commit()
        flash('Entry added successfully!')
    else:
        flash('Title and Description are required!')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    entry = Entry.query.get_or_404(id)
    if request.method == 'POST':
        form = request.form
        entry.title = form.get('title')
        entry.description = form.get('description')
        db.session.commit()
        flash('Entry updated successfully!')
        return redirect(url_for('index'))
    return render_template('update.html', entry=entry)

@app.route('/delete/<int:id>')
def delete(id):
    entry = Entry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted successfully!')
    return redirect(url_for('index'))

@app.route('/turn/<int:id>')
def turn(id):
    entry = Entry.query.get_or_404(id)
    entry.status = not entry.status
    db.session.commit()
    flash('Entry status updated!')
    return redirect(url_for('index'))

@app.errorhandler(Exception)
def error_page(e):
    return str(e), 500
