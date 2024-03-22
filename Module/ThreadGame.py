<<<<<<< HEAD
import threading
import time

_ThreadGameLocker=threading.Lock()
_isThreadGameLockerAcquired=False

class ThreadGame(object):
    def __init__(self):
        self.__lastOperationTime=time.time()
#
    def threadGameAcquire(self):
        global _ThreadGameLocker
        global _isThreadGameLockerAcquired

        _ThreadGameLocker.acquire()
        _isThreadGameLockerAcquired=True
#
    def threadGameRelease(self):
        global _ThreadGameLocker
        global _isThreadGameLockerAcquired

        if _isThreadGameLockerAcquired:
            _ThreadGameLocker.release()
            _isThreadGameLockerAcquired=False
#
    def threadGameIsAcquired(self):
        global _ThreadGameLocker
        global _isThreadGameLockerAcquired

        return _isThreadGameLockerAcquired
#
    def threadGameTryToAcquire(self):
        global _ThreadGameLocker
        global _isThreadGameLockerAcquired

        if _isThreadGameLockerAcquired:
            return False
        else:
            self.threadGameAcquire()
            return True
#
    def updateOperationTime(self):
        self.threadGameAcquire()

        self.__lastOperationTime=time.time()

=======
import threading
import time

_ThreadGameLocker=threading.Lock()
_isThreadGameLockerAcquired=False

class ThreadGame(object):
    def __init__(self):
        self.__lastOperationTime=time.time()
#
    def threadGameAcquire(self):
        global _ThreadGameLocker
        global _isThreadGameLockerAcquired

        _ThreadGameLocker.acquire()
        _isThreadGameLockerAcquired=True
#
    def threadGameRelease(self):
        global _ThreadGameLocker
        global _isThreadGameLockerAcquired

        if _isThreadGameLockerAcquired:
            _ThreadGameLocker.release()
            _isThreadGameLockerAcquired=False
#
    def threadGameIsAcquired(self):
        global _ThreadGameLocker
        global _isThreadGameLockerAcquired

        return _isThreadGameLockerAcquired
#
    def threadGameTryToAcquire(self):
        global _ThreadGameLocker
        global _isThreadGameLockerAcquired

        if _isThreadGameLockerAcquired:
            return False
        else:
            self.threadGameAcquire()
            return True
#
    def updateOperationTime(self):
        self.threadGameAcquire()

        self.__lastOperationTime=time.time()

>>>>>>> 5aba08ced5481b6f7896a7cef616b87c6e9f4d1e
        self.threadGameRelease()