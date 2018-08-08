# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import emoji_converter

from urllib.parse import parse_qs

HTML_INPUT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<title>Convert text with Weibo emoticons to Unicode</title>
<meta charset="UTF-8">
</head>
<body>
</center><h1>Emoji Converter</h1></center>
<form action = "simplehhtp.py" method= "post">
    <!-- <label for="WEIBO_ACCESS_TOKEN">Weibo Access Token:</label> -->
    <!-- <input type="password" id="WEIBO_ACCESS_TOKEN" name="WEIBO_ACCESS_TOKEN" required/> -->
    <label for="emoji_text">Text with Weibo Emoji:</label>
    <input type="text" id="emoji_text" name="emoji_text" required/>
    <input type="submit" value="Convert"/>
</form>
</body>
</html>
'''

HTML_OUTPUT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<title>Convert text with Weibo emoticons to Unicode</title>
<meta charset='utf-8'>
</head>
<body>
</center><h1>Emoji Converter</h1></center>
    <label for="converted_text">Converted text:</label>
<fieldset>
    %s
</fieldset>
</body>
</html>
'''

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(HTML_INPUT_TEMPLATE, "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        params = parse_qs(body)
        data = params["emoji_text"][0]
        self.send_response(200)
        self.end_headers()
        converted_text = emoji_converter.convert_text(data)
        message = (HTML_OUTPUT_TEMPLATE % converted_text)
        self.wfile.write(bytes(message, "utf-8"))


httpd = HTTPServer(('localhost', 5050), SimpleHTTPRequestHandler)
httpd.serve_forever()