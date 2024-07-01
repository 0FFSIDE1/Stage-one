This is the stage one task 
How to make a API call
url_endpoint = https://offside1.pythonanywhere.com/api/hello
url_endpoint_with_name = https://offside1.pythonanywhere.com/api/hello?visitor_name='YOUR_NAME'
or 
Do it this way 
url = https://offside1.pythonanywhere.com/api/hello?
parameters = {
'visitor_name': 'YOUR_NAME',
}
response = request.get(url, params=parameter)
