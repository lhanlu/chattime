Chattime contact book
======
This is a web app to display all details of users and contacts in the database.

##Quickstart

1. The complete URL to the hosted web application.
- http://34.220.89.238/5000
- if you are running the project in your local machine, you can use http://0.0.0.0/5000
2. A list of any third-party resources I made use of to complete this project.
Flask
Amazon lightsail 
Git
Rest
SQLalchemy


##What you can do
1. using "curl -d -H "Content-Type: application/json" -X GET http://34.220.89.238:5000/users/JSON", you can see the user list
2. using "curl -d -H "Content-Type: application/json" -X GET http://34.220.89.238:5000/users/users_id/contact/JSON" you can see the contact of each user
3. using command "curl -d '{ "name" : "name you want", "email" : "email you want"}'  -H "Content-Type: application/json" -X PUT http://34.220.89.238:5000/users/user_id/edit/", you can edit the user info to the database
4. using command "curl -d '{ "name" : "ZF", "email" : "123@321.com"}'  -H "Content-Type: application/json" -X POST http://34.220.89.238:5000/users/new" you can create a new user to the database
5. using command "curl -X DELETE http://34.220.89.238:5000/users/user_id/delete/" you can delete the user you choose
6. using command "curl -d '{ "name" : "name you want", "email" : "email you want"}'  -H "Content-Type: application/json" -X PUT http://34.220.89.238:5000/users/user_id/contact_id/edit/", you can edit each contact.
7. using command "curl -X DELETE http://34.220.89.238:5000/users/user_id/contact_id/delete/" , you can delete each contact.
8.  using command "curl -d '{ "name" : "ZF", "email" : "123@321.com"}'  -H "Content-Type: application/json" -X POST http://34.220.89.238:5000/users/users_id/contact/new/" you can create a new contact.


