from abc import ABC, abstractmethod

class DataParser(ABC):
    def _parse(self):
        self._open()
        self._dataparser()
        self._close()
    @abstractmethod
    def _dataparser(self):
        pass
    def _open(self):
        print('opening the file...')
    def _close(self):
        print('closing the file')
    
