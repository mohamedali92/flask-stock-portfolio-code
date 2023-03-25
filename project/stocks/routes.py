from sqlalchemy import select

from . import stocks_blueprint
from flask import current_app, render_template, request, session, flash, redirect, url_for, abort
from pydantic import BaseModel, validator, ValidationError
from project.models import Stock
from project import database
import click
from flask_login import current_user, login_user, login_required, logout_user
from datetime import date, datetime


# --------------
# Helper Classes
# --------------

class StockModel(BaseModel):
    """Class for parsing new stock data from a form."""
    stock_symbol: str
    number_of_shares: int
    purchase_price: float
    purchase_date: datetime

    @validator('stock_symbol')
    def stock_symbol_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()

    # @validator('purchase_date')
    # def purchase_date_check(cls, value):
    #     if value > datetime.now():
    #         raise ValueError("Purchase date can't be in the future")


# ------
# Routes
# ------

@stocks_blueprint.route('/')
def index():
    current_app.logger.info('Calling the index() function.')
    return render_template('stocks/index.html')


@stocks_blueprint.route('/add_stock', methods=['GET', 'POST'])
@login_required
def add_stock():
    if request.method == 'POST':
        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price'],
                purchase_date=datetime.strptime(request.form['purchase_date'], '%Y-%m-%d')
            )

            # Save the form data to the database
            new_stock = Stock(stock_symbol=stock_data.stock_symbol,
                              number_of_shares=stock_data.number_of_shares,
                              purchase_price=stock_data.purchase_price,
                              user_id=current_user.id,
                              purchase_date=datetime.strptime(request.form['purchase_date'], '%Y-%m-%d')
                              )
            database.session.add(new_stock)
            database.session.commit()

            flash(f"Added new stock ({stock_data.stock_symbol})!", 'success')
            current_app.logger.info(f"Added new stock ({request.form['stock_symbol']})!")

            return redirect(url_for('stocks.list_stocks'))
        except ValidationError as e:
            flash("Purchase date can't be in the future", category='error')
            print(e)

    return render_template('stocks/add_stock.html')


@stocks_blueprint.route('/stocks/')
@login_required
def list_stocks():
    stocks_owned_by_user = database.session.execute(
        select(Stock).
        where(Stock.user_id == current_user.id)

    ).scalars().all()
    current_account_value = 0.0
    for stock in stocks_owned_by_user:
        stock.get_stock_data()
        database.session.add(stock)
        current_account_value += stock.position_value
    database.session.commit()
    return render_template('stocks/stocks.html', stocks=stocks_owned_by_user, value=round(current_account_value, 2))



@stocks_blueprint.route('/stocks/<id>')
@login_required
def stock_details(id):
    stock = Stock.query.filter_by(id=id).first_or_404()

    if stock.user_id != current_user.id:
        abort(403)

    title, labels, values = stock.get_weekly_stock_data()
    return render_template('stocks/stock_details.html', stock=stock, title=title, labels=labels, values=values)



@stocks_blueprint.route("/chartjs_demo1")
def chartjs_demo1():
    return render_template('stocks/chartjs_demo1.html')
# -----------------
# Request Callbacks
# -----------------

# @stocks_blueprint.before_request
# def stocks_before_request():
#     current_app.logger.info('Calling before_request() for the stocks blueprint...')
#
#
# @stocks_blueprint.after_request
# def stocks_after_request(response):
#     current_app.logger.info('Calling after_request() for the stocks blueprint...')
#     return response
#
#
# @stocks_blueprint.teardown_request
# def stocks_teardown_request(error=None):
#     current_app.logger.info('Calling teardown_request() for the stocks blueprint...')


# ------------
# CLI Commands
# ------------

@stocks_blueprint.cli.command('create_default_set')
def create_default_set():
    """Create three new stocks and add them to the database"""
    stock1 = Stock('HD', '25', '247.29')
    stock2 = Stock('TWTR', '230', '31.89')
    stock3 = Stock('DIS', '65', '118.77')
    database.session.add(stock1)
    database.session.add(stock2)
    database.session.add(stock3)
    database.session.commit()


@stocks_blueprint.cli.command('create')
@click.argument('symbol')
@click.argument('number_of_shares')
@click.argument('purchase_price')
def create(symbol, number_of_shares, purchase_price):
    """Create a new stock and add it to the database"""
    stock = Stock(symbol, number_of_shares, purchase_price)
    database.session.add(stock)
    database.session.commit()
