import datetime
import os
import utils

import atoti as tt
import atoti.comparator as comparator
import constant as cc
import pandas as pd


def init_cube(session):
    df_trades = pd.concat(load_files(cc.DIR_TRADES))
    df_nettingsets = pd.concat(load_files(cc.DIR_NETTINGSETS))
    df_fxrates = pd.concat(load_files(cc.DIR_FXRATES))

    # ================
    # Stores
    # ================
    trades_store = load_store_from_dataframe(session=session,
                                             store_name=cc.TRADES_STORE,
                                             dataframe=df_trades,
                                             keys=[cc.TRADES_TRADE_ID, cc.ASOFDATE])

    netting_store = load_store_from_dataframe(session=session,
                                              store_name=cc.NETTING_SETS_STORE,
                                              dataframe=df_nettingsets,
                                              keys=[cc.NETTING_SETS_ID,
                                                    cc.ASOFDATE])

    fxrates_store = load_store_from_dataframe(session=session,
                                              store_name=cc.FOREX_STORE,
                                              dataframe=df_fxrates,
                                              keys=[cc.FOREX_COUNTER_CURRENCY, cc.ASOFDATE])

    counterparties_store = load_store_from_csv(session=session,
                                               store_name=cc.COUNTERPARTIES_STORE,
                                               path=cc.FILE_COUNTERPARTIES,
                                               keys=[cc.COUNTERPARTY_ID])

    books_store = load_store_from_csv(session=session,
                                      store_name=cc.BOOKS_STORE,
                                      path=cc.FILE_BOOKS,
                                      keys=[cc.BOOKS_BOOK_ID])

    pfeaddon_store = load_store_from_csv(session=session,
                                         store_name=cc.PFE_ADDON_STORE,
                                         path=cc.FILE_PFEADDON,
                                         keys=[cc.PFE_ASSET_CLASS, cc.PFE_MATURITY])

    # ================
    # References
    # ================
    trades_store.join(netting_store, mapping={cc.NETTING_SETS_ID: cc.NETTING_SETS_ID,
                                              cc.ASOFDATE: cc.ASOFDATE})
    trades_store.join(books_store, mapping={cc.BOOKS_BOOK_ID: cc.BOOKS_BOOK_ID})
    netting_store.join(counterparties_store, mapping={cc.COUNTERPARTY_ID: cc.COUNTERPARTY_ID})

    cube = utils.execute(session.create_cube, {'base_store': trades_store,
                                               'name': "CPR Atoti",
                                               'mode': "manual"},
                         event_name="Cube creation")

    h = cube.hierarchies
    lvl = cube.levels
    m = cube.measures

    # ================
    # Hierarchies
    # ================
    utils.log_event("Creating hierarchies")
    h[cc.NETTING_SETS_DIMENSION] = [
        netting_store[cc.NETTING_SETS_ID],
        netting_store[cc.NETTING_SETS_NAME],
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

    h[cc.ASOFDATE].slicing = True
    lvl[cc.ASOFDATE].comparator = comparator.DESC

    # h[cc.TRADES_MATURITY] = [
    #     trades_store[cc.TRADES_MATURITY]
    # ]

    h[cc.TRADES_DIMENSION] = [
        trades_store[cc.TRADES_TRADE_ID]
    ]

    # ================
    # Dimensions
    # ================
    h[cc.NETTING_SETS_DIMENSION].dimension = cc.NETTING_SETS_DIMENSION
    h[cc.PRODUCT_DIMENSION].dimension = cc.PRODUCT_DIMENSION
    h[cc.COUNTERPARTIES_DIMENSION].dimension = cc.COUNTERPARTIES_DIMENSION
    h[cc.GEOGRAPHY_DIMENSION].dimension = cc.GEOGRAPHY_DIMENSION
    h[cc.BOOKS_DIMENSION].dimension = cc.BOOKS_DIMENSION
    h[cc.ASOFDATE].dimension = cc.TIME_DIMENSION
    # h[cc.TRADES_MATURITY].dimension = cc.TIME_DIMENSION
    h[cc.TRADES_INPUT_CURRENCY].dimension = cc.CURRENCY_DIMENSION
    h[cc.NETTING_SETS_CURRENCY].dimension = cc.CURRENCY_DIMENSION
    h[cc.TRADES_DIMENSION].dimension = cc.TRADES_DIMENSION

    m["Collateral"] = netting_store["Collateral"]
    m["Collateral"].visible = False
    m["Collateral.SUM"] = tt.agg.sum(
        m["Collateral"],
        scope=tt.scope.origin(lvl["NettingSetId"]))

    # Net Positive Exposure
    m["Net Positive Exposure"] = tt.agg.long(trades_store["MarketValue"])

    # Counterparty Risk method 1
    cpr = m["Net Positive Exposure"].__sub__(m["Collateral.SUM"])
    m["CPR Method 1"] = tt.where(cpr.__ge__(0), cpr, 0)

    # tt.where(lvl[""])


# Retrieve AsOfDate from file name
def file_date(file):
    date = file[file.find('_') + 1: file.find('.')]
    return datetime.datetime.strptime(date, '%Y%m%d')


# Load all files in directory to dataframe
def load_files(directory):
    utils.log_event("Creating dataframe from files in " + directory)
    for filename in os.listdir(directory):
        df = pd.read_csv(directory + filename, low_memory=False)
        df[cc.ASOFDATE] = file_date(filename)
        yield df


# Load a store from a pandas dataframe
def load_store_from_dataframe(session, store_name, dataframe, keys):
    utils.log_event("Loading store " + store_name)
    loaded_store = utils.execute(session.read_pandas, {'dataframe': dataframe,
                                                       'keys': keys,
                                                       'store_name': store_name},
                                 event_name=store_name + " store load")
    print("-----------------")
    print(loaded_store.head())
    print("-----------------")
    return loaded_store


# Load a store directly from csv
def load_store_from_csv(session, store_name, path, keys):
    utils.log_event("Loading store " + store_name)
    loaded_store = utils.execute(session.read_csv, {'path': path,
                                                    'keys': keys,
                                                    'store_name': store_name},
                                 event_name=store_name + " store load")
    print("-----------------")
    print(loaded_store.head())
    print("-----------------")
    return loaded_store
