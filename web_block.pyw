from flask import Flask, jsonify, request
from datetime import datetime as dt
import time
import threading

app = Flask(__name__)

ip_localmachine = "127.0.0.1"
website_list = ["www.facebook.com", "facebook.com", "www.instagram.com", "instagram.com"]
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
start_time = dt.strptime("09:00:00", "%H:%M:%S").time()
end_time = dt.strptime("14:00:00", "%H:%M:%S").time()
block_active = True  # Toggle manually from dashboard


def blocker_loop():
    global block_active
    while True:
        now = dt.now().time()
        if block_active and start_time <= now <= end_time:
            with open(hosts_path, "r+") as file:
                content = file.read()
                for website in website_list:
                    if website not in content:
                        file.write(ip_localmachine + " " + website + "\n")
        else:
            with open(hosts_path, "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if not any(website in line for website in website_list):
                        file.write(line)
                file.truncate()
        time.sleep(10)


# Run blocker in the background
threading.Thread(target=blocker_loop, daemon=True).start()


@app.route("/status")
def status():
    return jsonify({
        "active": block_active,
        "websites": website_list,
        "start": start_time.strftime("%H:%M:%S"),
        "end": end_time.strftime("%H:%M:%S")
    })


@app.route("/toggle", methods=["POST"])
def toggle():
    global block_active
    block_active = not block_active
    return jsonify({"active": block_active})


@app.route("/update", methods=["POST"])
def update():
    global website_list, start_time, end_time
    data = request.get_json()

    if "site" in data:
        site = data["site"].strip()
        if site and site not in website_list:
            website_list.append(site)

    if "start" in data and "end" in data:
        start_time = dt.strptime(data["start"], "%H:%M").time()
        end_time = dt.strptime(data["end"], "%H:%M").time()

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)

