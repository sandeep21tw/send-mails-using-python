# simple program to send mail using the default email & password in .env file
# Completed: Works successfully

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from imghdr import what

load_dotenv()

def msg_body(email, password):

	msg = EmailMessage()
	title = input("\nWhat's the title of your email? ")
	recv_email = input("\nWhom do you want to send this mail to? ")
	content = input("\nType the message and press enter when you are done: ")

	msg["Subject"] = title
	msg["FROM"] = email
	msg["TO"] = recv_email
	msg.set_content(content)

	attachment(msg)
	send_message(email, password, msg)


def attachment(msg):
	print("\nDo you wanna add image or pdf to email (currently only these are supported) ")
	print("If yes, type in the path for image or pdf when prompted ")

	while True:
		option = input("\nWhat do you wanna add (image or pdf): ")

		if option.lower() in ['image', 'pdf']:
			file_data, file_name, main_type, file_type = open_file(option)
			msg.add_attachment(file_data, maintype=main_type, subtype=file_type, filename=file_name)

			add_more = input("\nDo you wanna add any more (image or pdf). Type 'yes' ")
			if add_more != 'yes':
				break
		else:
			print("\nOkay! We will proceed without adding any file.")
			break

	


def open_file(atype):
	url = input("\nEnter the full path of the file: ")

	with open(url, 'rb') as f:
		file_data = f.read()
		file_name = f.name

		if atype == 'image':
			file_type = what(file_name)
			main_type = atype
		elif atype == 'pdf':
			file_type = 'octet-stream'
			main_type = 'application'
		else:
			print("Error in open_file function.")


	return file_data, file_name, main_type, file_type


"""
def add_image():
	url = input("\nEnter the url of the image: ")

	with open(url, 'rb') as f:
		file_data = f.read()
		file_name = f.name
		file_type = ""
"""


def send_message(email, password, msg):
	with smtplib.SMTP('smtp.outlook.com', 587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()

		smtp.login(email, password)

		smtp.send_message(msg)


def main():
	email = os.getenv("EMAIL")
	password = os.getenv("PASS")

	"""
	print(email)
	print(password)
	"""

	msg_body(email, password)
	print("Done")

main()
