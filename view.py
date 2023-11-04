#описание метода в документации
from flask import Flask, render_template, request, redirect
import hashlib
import requests
import dotenv
import os
import logging

dotenv.load_dotenv()
#https://www.tinkoff.ru/kassa/develop/api/payments/init-description/

	# Define the payment information as a dictionary
	# Replace with your Tinkoff Merchant Terminal Key
	terminal_key = os.environ.get("TERMINALKEY")

	# Replace with your Tinkoff Merchant Secret Key
	secret_key = os.environ.get("TERMINALPASSWORD")

	values = {
			'Amount': str(cert.price*100)+'.00',#*100 потому что указывается сумма в копейках/ и в других методах почему то идёт  сразу с .00 а здесь без. глюк матрицы тинькофф...
			'Description': str(cert.product.title)+' ('+str(cert.count)+') шт.', # The order description
			'OrderId': str(cert.number_cert),
			'Password': secret_key,
			'TerminalKey': terminal_key
	}
	# Concatenate all values in the correct order
	concatenated_values = ''.join([values[key] for key in (values.keys())])

	# Calculate the hash using SHA-256 algorithm
	hash_object = hashlib.sha256(concatenated_values.encode('utf-8'))
	token = hash_object.hexdigest()
	logger.debug('shop.views(1159) buy token {} ',token)

	payment_data = {
			'TerminalKey':terminal_key,
			'OrderId': str(cert.number_cert),
			'Amount': str(int(cert.price*100)),#*100 потому что указывается сумма в копейках
			"Description": str(cert.product.title)+' ('+str(cert.count)+') шт.', # The order description
			"Language": "ru", # The language code (ru or en)
			"PayType": "O", # The payment type (O for one-time payment)
			"Recurrent": "N", # Indicates whether the payment is recurrent (N for no)
			# "CustomerKey": "1234567890", # The customer key (optional)

			'Token':token,
			'DATA': {
					'Phone': cert.investor.phone,
					'Email': cert.investor.email,
			},
			'PaymentMethod': {
					'Type': 'Mobile',
					'Data': {},
			},
			# данные чека
			'Receipt': {
					'Phone': str(cert.investor.phone),
					'Email': str(cert.investor.email),
					'Taxation':'usn_income',#упрощёнка
					'Items':[{  #https://www.tinkoff.ru/kassa/develop/api/receipt/#Items
							'Name':str(cert.product.title),
							'Quantity':str(cert.count),
							'Amount': str(int(cert.price*100)),
							'Tax':'none',#без НДС
							'Price':str(int(cert.product.price*100)),
					},]
					}, # your receipt data

			"SuccessURL": str(request.scheme+'://'+request.get_host()+"/youSuccess_path/?you_get="+str(your.pk)), # The URL for successful payments
			# "NotificationURL":request.scheme+'://'+request.get_host()+request.get_full_path()+'&CertId='+str(cert.pk), # The URL for payment notifications
			"FailURL":  str(request.scheme+'://'+request.get_host()+"/youFailURL_path/?you_get="+str(your.pk)), The URL for failed payments
	}

	#путь по которому мы отправляем свой запрос, прописан в документации банка
	url = "https://securepay.tinkoff.ru/v2/Init"

	response = requests.post(url, json=payment_data)
	logging.debug('shop.views Buy () Tinkoff response {}',response.json())

	if response.json()['Success']:
			payment_url = response.json()['PaymentURL']

			# Redirect the user to the payment form

			Certificate.objects.filter(id=cert.id).update(PaymentId=response.json()['PaymentId'])

			# отправляем пользователя на платёжную форму
			return redirect(payment_url)
	else:
			# result = False
			message = response.json()['Message']+' '+response.json()['Details']
			message.error(request, message)
			logging.debug('shop.views() buy response payment_url response {} ',response.json())