from sanic import Sanic
from sanic.response import html, json
import os

app = Sanic("WifiConfigApp")

# HTML form to capture WiFi credentials
html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>WiFi Configuration</title>
</head>
<body>
    <h2>Enter WiFi Credentials</h2>
    <form action="/config" method="post">
        <label for="ssid">SSID:</label>
        <input type="text" id="ssid" name="ssid"><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password"><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route("/")
async def index(request):
    return html(html_form)

@app.route("/config", methods=["POST"])
async def config(request):
    ssid = request.form.get('ssid')
    password = request.form.get('password')

    # Write the WiFi credentials to the wpa_supplicant.conf file
    wpa_supplicant_conf = f"""
    country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={{
        ssid="{ssid}"
        psk="{password}"
    }}
    """

    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as file:
        file.write(wpa_supplicant_conf)

    # Restart the wlan0 interface to apply the new configuration
    os.system("sudo wpa_cli -i wlan0 reconfigure")

    return json({"status": "success", "ssid": ssid})

if __name__ == "__main__":
    app.run(host="192.168.4.1", port=8000)
