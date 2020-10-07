""" Directories """
DIR_TRADES = "data/trades/"
DIR_NETTINGSETS = "data/nettingsets/"
DIR_FXRATES = "data/fxrates/"

#### Files ####
FILE_TRADES = "data/trades/trades_20200316.csv"
FILE_NETTING_SETS = "data/nettingsets/nettingSets_20200316.csv"
FILE_FXRATES = "data/fxrates/fxrates_20200316.csv"
FILE_COUNTERPARTIES = "data/counterparties_all.csv"
FILE_BOOKS = "data/books_all.csv"
FILE_PFEADDON = "data/pfeaddon.csv"


#### Dimensions ####
TRADES_DIMENSION = "Trades"
PRODUCT_DIMENSION = "Products"
NETTING_SETS_DIMENSION = "NettingSets"
COUNTERPARTIES_DIMENSION = "Counterparties"
BOOKS_DIMENSION = "Books"
TIME_DIMENSION = "Time"
CURRENCY_DIMENSION = "Currency"
GEOGRAPHY_DIMENSION = "Geography"

#### Stores
TRADES_STORE = "Trades"
NETTING_SETS_STORE = "NettingSets"
FOREX_STORE = "FOREX"
COUNTERPARTIES_STORE = "Counterparties"
BOOKS_STORE = "Books"
PFE_ADDON_STORE = "PFE"

#### Time
ASOFDATE = "AsOfDate"

#### Trades
TRADES_TRADE_ID = "TradeId"
TRADES_PRODUCT = "Product"
TRADES_NETTING_SETS_ID = "NettingSetId"
TRADES_BOOK_ID = "BookId"
TRADES_DIRECTION = "Direction"
TRADES_INPUT_CURRENCY = "InputCurrency"
TRADES_INSTRUMENT = "Instrument"
TRADES_ASSET_CLASS = "AssetClass"
TRADES_SUB_CLASS = "SubClass"
TRADES_OPTION_TYPE = "OptionType"
TRADES_UNDERLYING = "Underlying"
TRADES_MATURITY = "Maturity"
TRADES_NOTIONAL = "Notional"
TRADES_MARKET_VALUE = "MarketValue"

#### Netting Sets
NETTING_SETS_ID = "NettingSetId"
NETTING_SETS_NAME = "NettingName"
NETTING_SETS_TYPE = "NettingType"
NETTING_SETS_COUNTERPARTY_ID = "Counterparty"
NETTING_SETS_COLLATERAL = "Collateral"
NETTING_SETS_MTA = "MTA"
NETTING_SETS_CURRENCY = "InputCurrency"

#### Forex
FOREX_BASE_CURRENCY = "BaseCcy"
FOREX_COUNTER_CURRENCY = "CounterCcy"
FOREX_RATE = "FOREX"

#### Counterparties
COUNTERPARTY_ID = "CounterpartyId"
COUNTERPARTY_NAME = "CounterpartyName"
COUNTERPARTY_RATING = "Rating"
COUNTERPARTY_SECTOR = "Sector"
COUNTERPARTY_COUNTRY_OF_RISK = "CountryOfRisk"

##### Books
BOOKS_BOOK_ID = "BookId"
BOOKS_COMPANY = "Company"
BOOKS_DESK = "Desk"

#### PFE
PFE_ASSET_CLASS = "PFEAssetClass"
PFE_MATURITY = "PFEMaturity"
PFE_ADDON = "PFEAddon"