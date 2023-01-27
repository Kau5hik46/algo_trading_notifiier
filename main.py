from pathlib import Path

from account import TradingAccount
from adapter import NSEAdapter, Symbol
from security import Security


def main():
    # adapter = NSEAdapter(Symbol.BANK_NIFTY)
    # sec1 = Security(adapter)
    # sec1.ltp = 200
    # sec2 = Security(adapter)
    # sec2.ltp = 100
    # acc = TradingAccount()
    # acc.deposit(100000.00)
    # acc.buy(security=sec1, units=10)
    # acc.sell(security=sec2, units=20)

    # acc.__load__(Path("data.dump"))

    # acc.__dump__(Path("data.dump"))
    acc = TradingAccount()
    acc.__load__(Path("data.dump"))
    # print(acc)
    for i in acc.securities:
        print(i.ltp)


if __name__ == "__main__":
    main()
