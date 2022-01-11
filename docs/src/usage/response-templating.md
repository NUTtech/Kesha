# Response templating

You can use the GET parameters of your request in the body and headers of the
response.

To do this, in the body field or in the value of any header, add a string with
parameters in the format `Your body with the GET parameter $arg1`

Now on the request for example `/stub/?arg1=42` there will be a response with
the body `Your body with GET parameter 42`


