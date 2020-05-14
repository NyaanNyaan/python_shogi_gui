from subprocess import Popen, PIPE, STDOUT
from time import sleep
from iolib.nonblocking import NonBlockingStreamReader as NBSR
import shlex

# executing chlid processes with non-blocking stream
# initialize : exe = Exec(cmd,cwd)
#   cmd ... command cwd ... directory
# input      : exe.send(massage)
# read       : exe.receive()
# readlines  : exe.receive_lines()
# kill       : exe.kill()


class Exec:
    def __init__(self, cmd, cwd=None):
        self.p = Popen(
            cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=cwd
        )
        self.nbsr = NBSR(self.p.stdout)

    def send(self, massage):
        self.p.stdin.write((massage + '\n').encode())
        self.p.stdin.flush()
        print("send : " + massage)

    def receive(self):
        output = self.nbsr.readline()
        if not output:
            return None
        else:
            print("receive : " + output.decode(), end='')
            return output.decode()

    def receive_lines(self):
        while True:
            output = self.nbsr.readline()
            if output:
                yield output
            else:
                break

    def kill(self):
        self.nbsr.is_running = False
        self.p.kill()


if __name__ == "__main__":
    cmd = [".\\a.out"]
    print(cmd)
    exe = Exec(cmd)
    while True:
        while True:
            output = exe.receive()
            if(output):
                print(output, end='')
                break
            else:
                sleep(0.1)
                continue
        s = input()
        if(s == "kill"):
            exe.kill()
            break
        exe.send(s)
