from flask import Flask
app = Flask(__name__)

@app.route("/flask/")
def hello():
    return '''
<html>
<head>
	<title>top site</title>
	<link rel="stylesheet" href="../static/home/styles.css">
  <link rel="shortcut icon" href="../static/polls/favicon.ico.png"/>
  <meta charset="UTF-8">
</head>
<body>
 <p>Flask app<p>

</body>
</html>
'''