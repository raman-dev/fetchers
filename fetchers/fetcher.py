from abc import ABC, abstractmethod

class Fetcher(ABC):
    JSON = "fetcher.json"
    DICT = "fetcher.python.dict"
    @abstractmethod
    def fetch(self,url):
        pass

    @staticmethod
    def get_result_dict(self, results, format, url):
        return {"results":results,"format":format,"url":url}





