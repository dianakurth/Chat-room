from threading import Thread
import subprocess

# possible to add more clients by adding next threads
t1 = Thread(target=subprocess.run, args=(["python", "server.py"],))
t2 = Thread(target=subprocess.run, args=(["python", "client.py"],))
# t3 = Thread(target=subprocess.run, args=(["python", "client_2.py"],))

t1.start()
t2.start()
# t3.start()

t1.join()
t2.join()
# t3.join()
