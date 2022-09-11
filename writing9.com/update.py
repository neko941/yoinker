import time
exec(open("get_links.py").read())
time.sleep(3600)
exec(open("fetch_data.py").read())