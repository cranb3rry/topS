from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.




def index(request):
    return HttpResponse('''
<!DOCTYPE html>
<html>
<head>
<title>HLS Stream</title>
<style>
    body {
       
    }
</style>
</head>
<body>

</script>
<audio controls autoplay id="myaudio"><source src="http://noeight.net:888/top7.ogg" type="application/ogg" /></audio>

<script>
  var audio = document.getElementById("myaudio");
  audio.volume = 0.3;
</script>

<p id="radioadmin"></p>
<p id="radioartist"></p>
<p id="radiosong"></p>

<script>

var myRadioadmin = document.getElementById("radioadmin");
var myRadioartist = document.getElementById("radioartist");
var myRadiosong = document.getElementById("radiosong");
var myRadioartistPr = ''
var myRadiosongPr = '' 


setInterval(function() {
fetch('http://noeight.net:888/status-json.xsl')
.then((resp) => resp.json())
.then(function(json) {
  var stats = json.icestats
  var radio = stats.source


  if (radio.title != myRadiosongPr) {
    myRadiosong.innerHTML = radio.title;
    myRadiosongPr = radio.title;
    
  }

  if (radio.artist != myRadioartistPr) {
    myRadioartist.innerHTML = radio.artist;
    myRadioartistPr = radio.artist;
    
  }


    myRadioadmin.innerHTML = '';
    
    
    })  
}, 100);


  </script>

</body>
</html>''')