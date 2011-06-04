from __future__ import print_function
import subprocess
import sqlite3
import time
import threading
import minesocket


class MinecraftServer(object):
    """ A wrapper around the minecraft server """
    def __init__(self, jar_path, xmx = 512, xms = 512, cwd = "."):
        self.server = None
        self.jar = jar_path
        self.xmx = xmx
        self.xms = xms
        self.cwd = cwd
        self.err = None
        self.inp = None

    def start(self):
        self.server = self.start_server()
        self.inp = minesocket.InputServer(self.server.stdin, ("localhost", 1337))
        self.err = WriteThread(self.server.stderr, None)
        self.err.start()
        self.inp.run()

    def start_server(self, \
                     indata = subprocess.PIPE, \
                     outdata = subprocess.PIPE, \
                     errdata = subprocess.PIPE):
        Xmx = "-Xmx%dM" % self.xmx
        Xms = "-Xms%dM" % self.xms
        return subprocess.Popen(["java", "-jar", Xmx, Xms, self.jar], 
                                stdin=indata, 
                                stdout=outdata,
                                stderr=errdata,
                                cwd = self.cwd)
    def write(self, message):
        if self.server is None: return
        print(message, file=self.server.stdin)

    def shutdown(self):
        self.write("stop")
        self.inp.close()
        self.err.join(5)

class WriteThread(threading.Thread):
    def __init__(self, std, out):
        threading.Thread.__init__(self)
        self.out = open(out, "a+")
        self.std = std

    def run(self):
        while True:
            line = self.std.readline()
            if line:
                self.out.write(line)
            else:
                time.sleep(5)
        print("exiting")
        self.out.close()

