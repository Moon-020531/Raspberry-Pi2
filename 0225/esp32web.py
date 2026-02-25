from flask import Flask, render_template

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError 
except ImportError:
    from urllib2 import urlopen                  
    from urllib2 import HTTPError, URLError     


deviceIp = "192.168.0.17" 
portnum = "80"

base_url = "http://" + deviceIp + ":" + portnum
event_url = base_url + "/events"

app = Flask(__name__, template_folder='.')

@app.route('/events')
def getevents():
    data = "{}" 
    try:

        with urlopen(event_url, timeout=2) as u: 
            data = u.read().decode('utf-8')
    except HTTPError as e:
        print(f"HTTP error: {e.code}")
    except URLError as e:
   
        print(f"Network error: {e.reason}")
    except Exception as e:
        print(f"Generic error: {e}") 
        
    return data

@app.route('/') 
def dht22chart():
    return render_template("dhtchart.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)