from pathlib import Path

from accounting.account import TradingAccount


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
    acc.__load__(Path("data/data.dump"))
    # print(acc)
    for i in acc.securities:
        i.__update__()
        print(i.ltp)
    print(acc)


if __name__ == "__main__":
    main()
