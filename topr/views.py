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
		<p>
				<picture>
					<img src="/media/rn/1132.png" >
				</picture>
			</p>
		<p>
				<picture>
					<img src="/media/rn/567.png" >
				</picture>
			</p>
		<p>
				<picture>
					<img src="/media/rn/7.png" style="width:70%; height: :70%;">
				</picture>
			</p>
		<p>
				<picture>
					<img src="/media/rn/679.png" style="width:65%; height: :65%;">
				</picture>
			</p>

		<p>
				<picture>
					<img src="/media/rn/12351.png" style="width:60%; height: :60%;">
				</picture>
			</p>

			<p>
	<picture>
		<img src="/media/rn/68767d.png" style="width:80%; height: :80%;">
	</picture>
</p>
			<p>
					<picture>
					<img src="/media/rn/546.png" style="width:96%; height: :96%;">
					</picture>
				</p>
				
							
<p>
	<picture>
		<img src="/media/rn/qq.png" style="width:70%; height: :70%;">
	</picture>
</p>

</body>
</html>''')
