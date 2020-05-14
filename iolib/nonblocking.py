# http://eyalarubas.com/python-subproc-nonblock.html
from threading import Thread
from queue import Queue, Empty

class NonBlockingStreamReader:
    def __init__(self, stream):
        # stream...Popenクラス
        self._s = stream
        self._q = Queue()
        self.is_running = True

        # streamからの出力を_qに入れる関数
        def _populateQueue(stream, queue):
            while(self.is_running):
                # 返り値がb''でない間、stream.readlineをiterateする
                for line in iter(stream.readline, b''): 
                    queue.put(line)
                stream.close() # streamがkillされている時のために必要?
        
        self._t = Thread(target = _populateQueue, # スレッドを立ち上げる
                args = (self._s, self._q))
        self._t.daemon = True # 親がkillしたときにスレッドもkillする
        self._t.start()

    # 文字列がqueueにある時は文字列を出力、ない場合はNoneを返す
    def readline(self):
        try:
            return self._q.get_nowait()
        except Empty:
            return None