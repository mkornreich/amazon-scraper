from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            ret = self.function(*self.args, **self.kwargs)
            if not ret: break
