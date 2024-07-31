#!/usr/bin/python
# -*- coding: cp1251 -*-
import psycopg2
from flask import Flask, render_template, render_template_string
import logging
import webbrowser
import urllib.request


logger = logging.getLogger()
logging.basicConfig(filename='logger.log', level=logging.ERROR,
                    format=f'%(asctime)s %(levelname)s %(name)s: %(message)s')


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def main():
    return render_template('index.html', encoding='utf-8')


def load_stores(file, conn, cur):
    cur.execute("""DROP TABLE IF EXISTS stores""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stores(
        store_id varchar(4) PRIMARY KEY,
        store_name varchar(50) NOT NULL
    )
    """)
    conn.commit()

    with open(file, 'r', encoding='utf-8') as f:
        next(f)   # Skip the header row
        cur.copy_from(f, 'stores', sep=';')

    conn.commit()


def load_coupons(file, conn, cur):
    cur.execute("""DROP TABLE IF EXISTS coupons""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS coupons(
        store_id varchar(4) NOT NULL,
        date date NOT NULL,
        coupon_id varchar(10) PRIMARY KEY,
        promo_id varchar(50) NOT NULL,
        material int8 NOT NULL,
        billnum int8 NOT NULL
    )
    """)
    conn.commit()

    with open(file, 'r', encoding='utf-8') as f:
        next(f)   # Skip the header row
        cur.copy_from(f, 'coupons', sep=';')

    conn.commit()


def load_promos(file, conn, cur):
    cur.execute("""DROP TABLE IF EXISTS promos""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS promos(
        promo_id varchar(50) PRIMARY KEY,
        promo_name varchar(50) NOT NULL,
        promo_type varchar(10) NOT NULL,
        material int8 NOT NULL,
        discount int8 NOT NULL
        )
    """)
    conn.commit()

    with open(file, 'r', encoding='utf-8') as f:
        next(f)    # Skip the header row
        cur.copy_from(f, 'promos', sep=';')

    conn.commit()


def load_promo_types(file, conn, cur):
    cur.execute("""DROP TABLE IF EXISTS promo_types""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS promo_types(
        promo_type varchar PRIMARY KEY,
        promo_txt varchar NOT NULL
        )
    """)
    conn.commit()

    with open(file, 'r', encoding='utf-8') as f:
        next(f)   # Skip the header row
        cur.copy_from(f, 'promo_types', sep=';')

    conn.commit()


@app.route('/stores')
def stores():
    stores_file = 'stores.csv'
    stores_url = 'https://drive.google.com/uc?export=download&id=1QdFHOfPwaXP4Tcsl4qC8q_9zg2zLDPrL'
    return load(stores_url, stores_file)


@app.route('/coupons')
def coupons():
    coupons_file = 'coupons.csv'
    coupons_url = 'https://drive.google.com/uc?export=download&id=1K7NJeR1CJgXwDFykQ7tjND4ZZcOXL65S'
    return load(coupons_url, coupons_file)


@app.route('/promos')
def promos():
    promos_file = 'promos.csv'
    promos_url = 'https://drive.google.com/uc?export=download&id=15S7GkKpOcm3174jS_QFfHAdqAbvpZbFY'
    return load(promos_url, promos_file)


@app.route('/promo_types')
def promo_types():
    pt_file = 'promo_types.csv'
    pt_url = 'https://drive.google.com/uc?export=download&id=1qenV8oCW14AKQuYHPTGPoDSu-XAqfn1k'
    return load(pt_url, pt_file)


def load(url, file):
    try:
        conn = psycopg2.connect("host=localhost port=5432 dbname=stores_bd user=admin password=admin")
        cur = conn.cursor()
        urllib.request.urlretrieve(url, file)
        match file:
            case "stores.csv":
                load_stores(file, conn, cur)
            case "coupons.csv":
                load_coupons(file, conn, cur)
            case "promos.csv":
                load_promos(file, conn, cur)
            case "promo_types.csv":
                load_promo_types(file, conn, cur)
        logger.info('Success!')
        return render_template_string('<h2 align="center">Данные загружены успешно.</br>'
                                      '<a href="/index">Вернуться на главную</a></h2>')

    except Exception as e:
        logger.error('Error! Exception %s', e)
        return render_template_string('<h2 align="center">Данные не загружены.</br>'
                                      '<a href="/index">Вернуться на главную</a></h2>')


if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=False)
