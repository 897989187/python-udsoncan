from enum import Enum
import logging
from logging.handlers import RotatingFileHandler

class CommonFunc:
    @staticmethod
    def InitLogging(Logname: str, Classname: str, Path: str = './', WriteConsole: bool = True) -> logging.Logger:
        logger = logging.getLogger(Classname)
        logger.setLevel(level=logging.DEBUG)
        
        handler = RotatingFileHandler(Path + Logname, maxBytes=10 * 1024 * 1024, backupCount=1)
        handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s  - %(lineno)d - %(message)s')
        handler.setFormatter(formatter)
        
        if WriteConsole:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            logger.addHandler(console)
        
        logger.addHandler(handler)
        
        return logger
    
    # def TurnStrtoEnum(self, inputstr:str, enumtype:Enum): 
    #     try: 
    #         return enumtype[inputstr]
    #     except KeyError:
    #         log.error("no thsi element{inputstr} in enum {enumtype}")
    #     return None

# logger = CommonFunc.InitLogging('example.log', '', True)
# logger.debug("This is a debug message with a parameter: %s", "parameter_value")