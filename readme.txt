Ref: https://www.youtube.com/watch?v=Fc2O3_2kax8&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj

Django version downgraded to: 2.0.2

To setup Project interpreter in pyCharm:
1. Open settings 
2. select Project: Secure....
3. Project interpreter drop down menu then \python.exe

Home Page:- http://127.0.0.1:8000/SecureBank/
Login page:- http://127.0.0.1:8000/SecureBank/login/

Project Dir:

SecureBankSystem/
	SecuerBank/  <-- Our app
		static/		# contains bootstrap javascript and css.
			css/
			js/
			SecureBank/		# In this folder we will add our own javascript and css files.
		templates/
			SecureBank/ 	# This folder will contain all html files.
				login.html 
				home.html
			base.html		# Our base html file. All other html files extend this file.