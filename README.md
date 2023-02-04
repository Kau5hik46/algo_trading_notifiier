# algo_trading_notifiier
A continuous NSE market option chain tracker and notifier according to the strategy chosen.
  
## STRATEGY:
Using LTP to make the decision.  

## WORKFLOW:
1. get the data from the NSE  
2. process the data  
3. data goes through adapter -> notification -> strategy  
4. notification sent to user through telegram  

## HOW TO USE:
1. clone the repo  
2. open terminal with current directory at cloned repo  
3. In terminal, use:  
    pip install -r requirements.txt