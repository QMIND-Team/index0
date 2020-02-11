"""Transport module for sending strings to the manager."""

import socket
if __name__ == "__main__":
    from config import MANAGER_IP
else:
    from comms.config import MANAGER_IP

class Client():
    def __init__(self):
        """Client Constructor"""
        self.manager_ip = MANAGER_IP
        self.host = socket.gethostname() # Get local machine name
        self.port = 12345

    def send(self, msg: str):
        """Send string to Manager via the server module
        
        Works differently than Server.send()
        """
        
        srvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srvr.connect((self.host, self.port))

        srvr.send(msg.encode(encoding='UTF-8'))
        print('Sent message.')

        resp = []
        srvr.settimeout(5.0) # is there a better way to do this???
        while True: # receive data 1024 bytes at a time
            data = srvr.recv(1024).decode(encoding='UTF-8')
            if data == '':
                break
            resp.append(data) # append decoded string
        
        if resp is None: # shut down and retry
            srvr.close()
            return None

        response = ''.join(resp)

        srvr.close()

        return response
