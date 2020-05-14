import iolib.inoutlib
import time


class UsiWrapper:
    def __init__(self, soft_name, soft_dir, setoption):
        self.soft_name = soft_name
        self.soft_dir = soft_dir
        self.setoption = setoption
        self.exec = iolib.inoutlib.Exec(soft_name, soft_dir)
        self.init()

    # send massage to engine
    def send(self, massage):
        self.exec.send(massage)

    # receive massage from engine
    def receive(self):
        ret = self.exec.receive()
        if ret == None:
            return None
        else:
            return ret.rstrip()

    # send str_send, and verify receiving str_recv
    def verify(self, str_send, str_recv):
        self.send(str_send)
        start = time.time()
        while True:
            if time.time() - start > 10.0:
                raise RuntimeError('Unreceived : ' + str_recv)
            buf = self.receive()
            if buf == None:
                time.sleep(0.01)
            if buf == str_recv:
                break

    # initialize engine
    def init(self):
        self.verify('usi', 'usiok')
        for line in self.setoption:
            self.send(line)
            time.sleep(0.01)
        self.verify('isready', 'readyok')
        self.send('usinewgame')

    # start engine
    def go(self, sfen=None):
        if sfen != None:
            self.send('position sfen ' + sfen)
        self.send('go infinite')

    # stop engine
    def stop(self):
        self.send('stop')

    # kill engine
    def kill(self):
        self.exec.kill()


if __name__ == '__main__':
    from config import soft_name, soft_dir, setoption
    exe = UsiWrapper(soft_name, soft_dir, setoption)
    exe.go()
    start = time.time()
    while True:
        if time.time() - start > 10:
            break
        buf = exe.receive()
        time.sleep(0.01)
    exe.kill()
