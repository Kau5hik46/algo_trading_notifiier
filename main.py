from pathlib import Path

from adapter.adapter import NSEAdapter
from entity.underlying_symbols import Symbol
from manager.strangle import Strangle


def main():
    adapter = NSEAdapter(Symbol.BANK_NIFTY)
    strategy = Strangle()
    strategy.__set_config__()
    path = Path('data', strategy.__str__())
    strategy.begin_strategy(path)
    for security in strategy.account.securities:
        security.__update__(adapter)

    print(strategy.open_positions, strategy.account)
    strategy._save_strategy(path)


if __name__ == "__main__":
    main()
