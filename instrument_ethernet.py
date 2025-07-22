import socket

class Command_Ethernet:
    PORT = 5025

    def __init__(self, host, timeout=3):
        self.host = host
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM,
                                    socket.IPPROTO_TCP)
        #self.timeout = 0
        self.set_timeout(timeout)

    def connect(self):
        self.socket.connect((self.host, self.PORT))

    def close(self):
        self.socket.close()

    def write(self, cmd):
        self._send(cmd)

    def read(self, num_bytes=1024):
        # self._send('READ?')
        return self._recv(num_bytes)

    def query(self, cmd, buffer_size=1024*1024):
        self.write(cmd)
        return self.read(buffer_size)

    def set_timeout(self, timeout):
        if timeout < 1e-3 or timeout > 3:
            raise ValueError('Timeout must be >= 1e-3 (1ms) and <= 3 (3s)')

        self.timeout = timeout
        self.socket.settimeout(self.timeout)

    def _send(self, value):
        encoded_value = ('%s\n' % value).encode('ascii')
        self.socket.send(encoded_value)

    def _recv(self, byte_num):
        value = self.socket.recv(byte_num)
        return value.decode('ascii')
