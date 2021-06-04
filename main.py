from flask import Flask, request, jsonify
from random import randint
import json, requests
import logging
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(dbname='german_db_16', user='german_16', password='123', host='116.203.27.46', port='5055')
cursor = conn.cursor()

# Получить список инвесторов
@app.route('/get_investors', methods=['GET'])
def get_investors():

    investor_list = []

    if conn:
        print('CON =====')

        p_query = """Select name, surname, investor_type.investype, count_pies, email, address
        from investor inner join investor_type
        on investor_type.id = investor.investype"""
        cursor.execute(p_query)
        investors_data = cursor.fetchall()

        for investor in investors_data:

            inv_name = investor[0]
            inv_surname = investor[1]
            inv_type = investor[2]
            inv_pies = investor[3]
            inv_email = investor[4]
            inv_address = investor[5]

            print('inv_name ', inv_name)

            investor_obj = {'inv_name': inv_name,
                            'inv_surname': inv_surname,
                            'inv_type': inv_type,
                            'inv_pies': inv_pies,
                            'inv_email': inv_email,
                            'inv_address': inv_address}

            investor_list.append(investor_obj)

            print(investor)

    return jsonify(investor_list)


# Добавить инвестора
@app.route('/add_investors', methods=['POST'])
def add_investors():

    name = request.form.get('name')
    surname = request.form.get('surname')
    investype = request.form.get('investype')
    count_pies = request.form.get('count_pies')
    email = request.form.get('email')
    address = request.form.get('address')

    if conn:
        base_data = (name, surname, investype, count_pies, email, address)
        p_query = """INSERT INTO public.investor (name, surname, investype, count_pies, email, address) 
        VALUES (%s,%s,%s,%s,%s,%s)"""
        cursor.execute(p_query, base_data)
        conn.commit()

    result = 'Investor added successfully!'
    return result


# Добавление баланса в таблицу, подсчет цены пая
@app.route('/pie_price', methods=['POST'])
def pie_price():

    balance = int(request.form.get('balance'))

    if conn:
        base_data = (balance,)
        actual_balance = "INSERT INTO public.balance (balance) VALUES (%s)"
        cursor.execute(actual_balance, base_data)
        conn.commit()

        summa_pies = "SELECT SUM(count_pies) FROM public.investor"
        cursor.execute(summa_pies)
        sum_pies = cursor.fetchone()

        pie_price = balance // sum_pies[0]
        result = 'Actual pie price: ' + str(pie_price)
        return result


