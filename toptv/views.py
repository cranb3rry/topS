from django.shortcuts import render

from django.http import HttpResponse



def index(request):
    return HttpResponse('''<!DOCTYPE html>
<html>
<head>

</head>

<body>
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<video id="video"></video>
<script>
  if(Hls.isSupported()) {
    var video = document.getElementById('video');
    var hls = new Hls();
    hls.loadSource('https://video-dev.github.io/streams/x36xhzz/x36xhzz.m3u8');
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED,function() {
      video.play();
  });
 }
</script>
</body>
</html> ''')

def hls(request):
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
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<video id="video" width="1280" height="720" controls></video>
<script>
  if(Hls.isSupported()) {
    var video = document.getElementById('video');
    var hls = new Hls();
    hls.loadSource('http://94.158.191.180:81/hls/test.m3u8');
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED,function() {
      video.play();
  });
 }
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

setInterval(function() {
fetch('http://noeight.net:888/status-json.xsl')
.then((resp) => resp.json())
.then(function(json) {
  var stats = json.icestats
  var radio = stats.source
    myRadioadmin.innerHTML = '';
    myRadioartist.innerHTML = radio.artist;
    myRadiosong.innerHTML = radio.title;
    })  
}, 100);


  </script>

</body>
</html>''')