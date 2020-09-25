import datetime
import os

import atoti as tt
import constant as cc
import pandas as pd


def init_cube(session):
    df_trades = pd.concat(load_files(cc.DIR_TRADES))
    df_nettingsets = pd.concat(load_files(cc.DIR_NETTINGSETS))
    df_fxrates = pd.concat(load_files(cc.DIR_FXRATES))

    ''' Stores '''
    trades_store = session.read_pandas(df_trades, keys=[cc.TRADES_TRADE_ID, cc.ASOFDATE], store_name="Trades")
    nettingSets_store = session.read_pandas(df_nettingsets, keys=[cc.NETTING_SETS_ID, cc.ASOFDATE],
                                            store_name="NettingSets")
    fxrates_store = session.read_pandas(df_fxrates, keys=[cc.FOREX_COUNTER_CURRENCY, cc.ASOFDATE], store_name="FXRates")
    counterparties_store = session.read_csv(cc.FILE_COUNTERPARTIES, keys=[cc.COUNTERPARTY_ID])
    books_store = session.read_csv(cc.FILE_BOOKS, keys=[cc.BOOKS_BOOK_ID])
    pfeaddon_store = session.read_csv(cc.FILE_PFEADDON, keys=[cc.PFE_ASSET_CLASS, cc.PFE_MATURITY])

    ############ References ###############
    trades_store.join(nettingSets_store, mapping={cc.NETTING_SETS_ID: cc.NETTING_SETS_ID,
                                                  cc.ASOFDATE: cc.ASOFDATE})
    trades_store.join(books_store, mapping={cc.BOOKS_BOOK_ID: cc.BOOKS_BOOK_ID})
    nettingSets_store.join(counterparties_store, mapping={cc.COUNTERPARTY_ID: cc.COUNTERPARTY_ID})
    cube = session.create_cube(trades_store, "cpr_atoti", mode="manual")

    h = cube.hierarchies
    lvl = cube.levels
    m = cube.measures

    print(trades_store.head())

    ############# Hierarchies #################
    h[cc.NETTING_SETS_DIMENSION] = [
        nettingSets_store[cc.NETTING_SETS_ID],
        nettingSets_store[cc.NETTING_SETS_NAME],
    ]

    h[cc.PRODUCT_DIMENSION] = [
        trades_store[cc.TRADES_PRODUCT],
        trades_store[cc.TRADES_ASSET_CLASS],
        trades_store[cc.TRADES_SUB_CLASS],
        trades_store[cc.TRADES_UNDERLYING]
    ]

    h[cc.COUNTERPARTIES_DIMENSION] = [
        counterparties_store[cc.COUNTERPARTY_NAME]
    ]

    h[cc.GEOGRAPHY_DIMENSION] = [
        counterparties_store[cc.COUNTERPARTY_COUNTRY_OF_RISK]
    ]

    h[cc.BOOKS_DIMENSION] = [
        books_store[cc.BOOKS_DESK],
        books_store[cc.BOOKS_BOOK_ID]
    ]

    h[cc.TRADES_INPUT_CURRENCY] = [
        trades_store[cc.TRADES_INPUT_CURRENCY]
    ]

    h[cc.NETTING_SETS_CURRENCY] = [
        trades_store[cc.NETTING_SETS_CURRENCY]
    ]

    h[cc.ASOFDATE] = [
        trades_store[cc.ASOFDATE]
    ]

    h[cc.TRADES_MATURITY] = [
        trades_store[cc.TRADES_MATURITY]
    ]

    ############# Dimension #################
    h[cc.NETTING_SETS_DIMENSION].dimension = cc.NETTING_SETS_DIMENSION
    h[cc.PRODUCT_DIMENSION].dimension = cc.PRODUCT_DIMENSION
    h[cc.COUNTERPARTIES_DIMENSION].dimension = cc.COUNTERPARTIES_DIMENSION
    h[cc.GEOGRAPHY_DIMENSION].dimension = cc.GEOGRAPHY_DIMENSION
    h[cc.BOOKS_DIMENSION].dimension = cc.BOOKS_DIMENSION
    h[cc.ASOFDATE].dimension = cc.TIME_DIMENSION
    h[cc.TRADES_MATURITY].dimension = cc.TIME_DIMENSION
    h[cc.TRADES_INPUT_CURRENCY].dimension = cc.CURRENCY_DIMENSION
    h[cc.NETTING_SETS_CURRENCY].dimension = cc.CURRENCY_DIMENSION

    m["Collateral"] = nettingSets_store["Collateral"]
    m["Collateral"].visible = False
    m["Collateral.SUM"] = tt.agg.sum(
        m["Collateral"],
        scope=tt.scope.origin(lvl["NettingSetId"]))

    # Net Positive Exposure
    m["Net Positive Exposure"] = tt.agg.long(trades_store["MarketValue"])

    # Counterparty Risk method 1
    cpr = m["Net Positive Exposure"].__sub__(m["Collateral.SUM"])
    m["CPR Method 1"] = tt.where(cpr.__ge__(0), cpr, 0)

    tt.where(lvl[""])

    # PFE Addon
    # m[PFE Addon] = "pfeaddon_store"


def file_date(file):
    date = file[file.find('_') + 1: file.find('.')]
    return datetime.datetime.strptime(date, '%Y%m%d')


def load_files(directory):
    for filename in os.listdir(directory):
        df = pd.read_csv(directory + filename, low_memory=False)
        df[cc.ASOFDATE] = file_date(filename)
        yield df
