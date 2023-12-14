from flask import Flask, render_template, flash, url_for, request
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SomthingWhatNoICanGuess'


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
    return render_template("index.html")


@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    offer = CantorOffer()
    offer.load_offer()

    if request.method == 'GET':
        return render_template('exchange.html', offer=offer)
    else:
        flash("Debug mode")
        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        if currency in offer.denied_codes:
            flash(f"The currency {currency} cannot be accepted")
        elif offer.get_by_code(currency) == 'unknown':
            flash(f"the selected currency is unknown and cannot be accepted")
        else:
            flash(f"Request to chchange {currency} was accepted")

        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        return render_template('exchange_results.html', currency=currency, amount=amount,
                               currency_info=offer.get_by_code(currency))


if __name__ == '__main__':
    app.run(debug=True)
