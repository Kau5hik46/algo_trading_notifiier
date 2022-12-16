__author__ = "Lavanya Naresh"
__modified__ = "16-Dec-2022"


from adapter import *
"""
objective:
Basically a logger
It notifies when the certain condition as stated in strategy.py is satisfied.

STEPS:
1. get the data from adapter.py for the NSE LTP
2. using that LTP data check, make arithmetic operations with strategy.py
3. check for the condition fulfilment.
4. notify if condition fulfilled then timeout else timeout directly
5. repeat loop
"""


def notification(data: dict) -> int:
    """
    Function
    Helper function that takes input data and makes decision to send notification
    
    Params
    ------
    data: dict
        input data
    
    Returns
    -------
    result: int
        Should the output be bool? I think it should be integer (one hot encoding kind of results)
        1 -> put
        2 -> call
        3 -> neutral
        ...
        1 to N where N is the possible number of decisions that can be taken at a position
    """
    result = None
    # some code here that does the required tasks
    return result
    

if __name__ == "__main__":
    # some code here that does the required tasks
    pass