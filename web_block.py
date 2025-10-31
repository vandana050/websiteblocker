import time
from datetime import datetime as dt

ip_localmachine = "127.0.0.1"
website_list = ["www.facebook.com", "facebook.com", "www.instagram.com", "instagram.com"]
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"

start_time = dt.strptime("09:00:00", "%H:%M:%S").time()
end_time = dt.strptime("14:00:00", "%H:%M:%S").time()

while True:
    now = dt.now()
    current_time = now.time()

    if start_time <= current_time <= end_time:
        print("Working hours: blocking sites")
        with open(hosts_path, "r+") as file:
            content = file.read()
            for website in website_list:
                if website not in content:
                    file.write(ip_localmachine + " " + website + "\n")
    else:
        print("Non-working hours: unblocking sites")
        with open(hosts_path, "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if not any(website in line for website in website_list):
                    file.write(line)
            file.truncate()

    time.sleep(10)
