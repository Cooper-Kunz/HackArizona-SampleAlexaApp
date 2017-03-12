Here is a custom Amazon Alexa skill created at HackArizona 2017, The University of Arizona's Hackathon, named MyCaretaker. 

Ngrok example usage...
When running a Flask or Django application you typically recieve a message saying something like, "Your application is now running on 127.0.0.0:8000".
Notice that the application is running on port 8000.
In order to now use Ngrok go to the directory of the project that is running and call Ngrok like this...
./ngrok_linux http 8000, where http is the protocol and 8000 is the port number. 
Ngrok should respond by saying, application is now running on, "https://459fb52f.ngrok.io", and boom... If you visit that URL you should see your application running on the web, with an https connection, which is required by Alexa applications.

[![Demo Alexa Application, My Caretaker - University of Arizona Hackathon 2017](https://img.youtube.com/vi/9vxlIPH3TnQ/0.jpg)](https://www.youtube.com/watch?v=9vxlIPH3TnQ "Alexa Demo Application")
