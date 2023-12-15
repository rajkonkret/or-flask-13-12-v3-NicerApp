from flask import Flask, render_template, flash, request, g, redirect, url_for
import sqlite3
from datetime import datetime

app_info = {
    'db_file': 'data/cantor.db'
}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SomthingWhatNoICanGuess'


def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app_info['db_file'])
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        print(error)


class Currency:

    def __init__(self, code, name, flag):
        self.code = code
        self.name = name
        self.flag = flag

    def __repr__(self):
        return f'<Currency {self.code}>'


class CantorOffer:
    def __init__(self):
        self.currencies = []
        self.denied_codes = []

    def load_offer(self):
        self.currencies.append(Currency('USD', 'Dollar', 'flag_usa.png'))
        self.currencies.append(Currency('EUR', 'Euro', 'flag_euro.png'))
        self.currencies.append(Currency('JPY', 'Yen', 'flag_japan.png'))
        self.currencies.append(Currency('GBP', 'Pound', 'flag_uk.png'))
        self.denied_codes.append('USD')

    def get_by_code(self, code):
        for currency in self.currencies:
            if currency.code == code:
                return currency
        return Currency('unknown', 'unknown', 'flag_pirat.png')


@app.route('/')
def index():
    return render_template("index.html", active_menu="home")


@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    offer = CantorOffer()
    offer.load_offer()

    if request.method == 'GET':
        return render_template('exchange.html', active_menu="exchange", offer=offer)
    else:
        flash("Debug mode")
        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        if currency in offer.denied_codes:
            flash(f"The currency {currency} cannot be accepted")
        elif offer.get_by_code(currency) == 'unknown':
            flash(f"the selected currency is unknown and cannot be accepted")
        else:
            db = get_db()
            # sql_command = "insert into transactions(currency, amount, user) values('USD',300,'admin');"
            sql_command = "insert into transactions(currency, amount, user) values(?,?,?)"
            db.execute(sql_command, [currency, amount, 'admin'])
            db.commit()
            flash(f"Request to chchange {currency} was accepted")

        return render_template('exchange_results.html', active_menu="exchange", currency=currency, amount=amount,
                               currency_info=offer.get_by_code(currency))


@app.route('/history')
def history():
    db = get_db()
    sql_command = 'select id, currency, amount, trans_date from transactions;'
    cur = db.execute(sql_command)
    transactions = cur.fetchall()

    return render_template('history.html', active_menu="history", transactions=transactions)


@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    db = get_db()
    sql_statement = 'delete from transactions where id = ?;'
    db.execute(sql_statement, [transaction_id])
    db.commit()

    return redirect(url_for('history'))


@app.route('/edit_transaction/<int:transaction_id>')
def edit_transaction(transaction_id):
    offer = CantorOffer()
    offer.load_offer()
    db = get_db()

    if request.method == 'GET':
        sql_statement = "select id, currency, amount from transactions where id=?;"
        cur = db.execute(sql_statement, [transaction_id])
        transaction = cur.fetchone()

        if transaction == None:
            flash('No such transaction!')
            return redirect(url_for('history'))
        else:
            return render_template('edit_transaction.html', transaction=transaction,
                                   active_menu="history", offer=offer)



    else:
        flash("Debug mode")
        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        if currency in offer.denied_codes:
            flash(f"The currency {currency} cannot be accepted")
        elif offer.get_by_code(currency) == 'unknown':
            flash(f"the selected currency is unknown and cannot be accepted")
        else:
            db = get_db()
            # sql_command = "insert into transactions(currency, amount, user) values('USD',300,'admin');"
            sql_command = "insert into transactions(currency, amount, user) values(?,?,?)"
            db.execute(sql_command, [currency, amount, 'admin'])
            db.commit()
            flash(f"Request to chchange {currency} was accepted")

        return render_template('exchange_results.html', active_menu="exchange", currency=currency, amount=amount,
                               currency_info=offer.get_by_code(currency))


if __name__ == '__main__':
    app.run(debug=True)
