from flask import Flask
app = Flask(__name__)

@app.route("/flask/")

def hello():
    return '''

<html>
<head>
	<title>flask</title>
	<link rel="stylesheet" href="../static/home/styles.css">
  <link rel="shortcut icon" href="../static/polls/favicon.ico.png"/>
  <meta charset="UTF-8">
</head>
<body>
 <p>Flask a211p1<p>

 	<script type="text/javascript">
 		
 		var ws = new WebSocket('ws://noeight.net:8080/');

		ws.onmessage = function(event) {

  		console.log(event.data);
			};

 	</script>



</body>
</html>


'''