class Logger:
    __instance = None
    def __new__(cls,file_name):
        if(cls.__instance==None):
            cls.__instance = super().__new__(cls)
            cls.__instance.file_name = file_name
            cls.__instance.log_count=0
            return cls.__instance
        else:
            return cls.__instance
    def log(self,msg:str):
        print(f"Logging {msg} in {self.file_name}")
        self.log_count += 1
    def get_log_count(self)->int:
        return self.log_count

log1 = Logger("app.log")
log1.log("Hey")
print(log1.get_log_count())

log2 = Logger("app2.log")
log2.log("Bye")
print(log2.get_log_count())


log3 = Logger("app.log")
log3.log("Good")
print(log3.get_log_count())