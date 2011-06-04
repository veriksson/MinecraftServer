from flask import Flask, render_template
import socket
app = Flask(__name__)
app.debug =True
@app.route("/")
def index():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(b"help", ("localhost", 1337))
    recv, address = s.recvfrom(256)
    return render_template("index.html", message = recv)

@app.route("/players/{name}")
def players():
    return "cc"
    

if __name__ == "__main__":
    app.run()
    
