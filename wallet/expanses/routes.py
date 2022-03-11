from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from wallet import db
from wallet.database_connector import Transaction
from wallet.expanses.forms import ExpanseForm

expans = Blueprint('expanses', __name__)

@expans.route("/expanses")
@login_required
def expanses():
    transactions = Transaction.query.filter_by(owner=current_user)
    return render_template('expanses.html', title="Expanses", transactions=transactions)

@expans.route("/expanses/new", methods=['GET','POST'])
@login_required
def new_expanse():
    form = ExpanseForm()
    if form.validate_on_submit():
        expanse = Transaction(name=form.name.data, value=form.value.data, category=form.category.data, date=form.date.data, owner=current_user)
        db.session.add(expanse)
        db.session.commit()        
        flash('Expanse already added!', 'success')
        return redirect(url_for('expanses.expanses'))
    return render_template('new_expanse.html', title="New Expanse", form=form)
    
@expans.route("/expanses/<int:transaction_id>")
@login_required
def expanse(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    return render_template('expanse.html', transaction=transaction)

@expans.route("/expanses/<int:transaction_id>/update")
@login_required
def update_expanse(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.owner != current_user:
        abort(403)
    form = ExpanseForm()
    return render_template('new_expanse.html', title="Update Expanse", form=form)
