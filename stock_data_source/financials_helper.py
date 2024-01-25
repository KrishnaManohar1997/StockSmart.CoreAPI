from stock.models import StockFinancial, Stock
from stock_data_source.twelve_data import FinancialDataService
from stock.constants import FinancialType, StockIncomePeriod
from time import sleep

from stock_data_source.twelve_data.ticker_data_service import TickerDataService


fds = FinancialDataService()
invalid_ticker_symbols = [
    "CMSINFO",
    "KHFM",
    "MAPMYINDIA",
    "DYNAMIC",
    "DCI",
    "AVROIND",
    "MDL",
    "BRIGHT",
    "SIDDHIKA",
    "DRSDILIP",
    "MOGSEC",
    "REXPIPES",
    "DIGJAMLMTD",
    "HIGHGROUND",
    "NANDANI",
    "SHREMINVIT",
    "TARACHAND",
    "UNIINFO",
    "JETKNIT",
    "OSIAHYPER",
    "NCPSESDL24",
    "VASA",
    "RELIABLE",
    "RATEGAIN",
    "VERA",
    "E2E",
    "AAATECH",
    "MAHICKRA",
    "MILTON",
    "MITCON",
    "ABINFRA",
    "HECPROJECT",
    "MPTODAY",
    "INDIGRID",
    "DEVIT",
    "AMBANIORG",
    "LGHL",
    "PRITI",
    "ACCORD",
    "MEDPLUS",
    "GRETEX",
    "KKVAPOALF",
    "CADSYS",
    "TRANSWIND",
    "BCONCEPTS",
    "DATAPATTNS",
    "OMFURN",
    "AVSL",
    "NPBET",
    "SIGMA",
    "BIRET",
    "AISL",
    "WEWIN",
    "DUDIGITAL",
    "LATTEYS",
    "EMBASSY",
    "LAKPRE",
    "GIRIRAJ",
    "SRIRAM",
    "PASHUPATI",
    "PIGL",
    "BBTCL",
    "NPST",
    "SPECTRHARE",
    "DSML",
    "SILVERTUC",
    "RMDRIP",
    "AILIMITED",
    "NARMADA",
    "ACEINTEG",
    "QUADPRO",
    "WALPAR",
    "PAVNAIND",
    "PULZ",
    "BEWLTD",
    "HPIL",
    "KSOLVES",
    "DESTINY",
    "MKPL",
    "JUNIORBEES",
    "AURDIS",
    "SHUBHLAXMI",
    "SMVD",
    "PGINVIT",
    "LEXUS",
    "BETA",
    "SURANI",
    "BMETRICS",
    "THEJO",
    "HPAL",
    "GUJRAFFIA",
    "SHRIRAMPPS",
    "OSWALSEEDS",
    "SUPRIYA",
    "JALAN",
    "SKSTEXTILE",
    "ATALREAL",
    "AMJUMBO",
    "EMAMIPAP",
    "ASLIND",
    "ARTEMISMED",
    "BTML",
    "TALWGYM",
    "VMARCIND",
    "UWCSL",
    "FELIX",
    "SVEES",
    "KOTAKIT",
    "IRBINVIT",
    "RAMSARUP",
    "JAKHARIA",
    "VSCL",
    "SONAHISONA",
    "SOLEX",
    "INNOVATAR",
    "MAFANG",
    "UNITY",
    "BOHRA",
    "SSINFRA",
    "PARIN",
    "CONTI",
    "PROLIFE",
    "WFL",
    "EMKAYTOOLS",
    "INNOVATIVE",
    "KRITIKA",
    "ZODIAC",
    "SHARIABEES",
    "METROBRAND",
    "VCL",
    "UCL",
    "SONAMCLOCK",
    "SOFTTECH",
    "KOTAKPSUBK",
    "MINDSPACE",
    "PARTYCRUS",
    "DRL",
    "UNITEDPOLY",
    "PERFECT",
    "AVG",
    "MHHL",
    "JAINAM",
    "SARVESHWAR",
    "CMMIPL",
    "CROWN",
    "TIRUPATI",
    "SHIVAUM",
    "ASCOM",
    "SECURCRED",
    "KSHITIJPOL",
    "MANAV",
    "DIAPOWER",
    "SECL",
]  # noqa


def store_income():
    failed_tickers_list = []
    # Number of credits user per Call -> 100
    stock_symbol_id_map = dict(
        Stock.objects.order_by("symbol").values_list("symbol", "id")
    )

    requests_made = 0
    num_calls = 0
    for stock, id in stock_symbol_id_map.items():
        try:
            financial_objs = []
            num_calls += 1

            for income_period, _ in StockIncomePeriod.choices:
                if requests_made >= 6:
                    print("Resting for a minute .... Calls Made -> ", requests_made)
                    sleep(60)
                    requests_made = 0

                requests_made += 1
                response = fds.get_ticker_income_statement(stock, income_period)
                response_data = response.json()
                if not response_data.get("meta"):
                    print("Error", stock, income_period, response_data.get("message"))
                    failed_tickers_list.append(
                        (stock, income_period, response_data.get("message"))
                    )
                    continue
                for statement in response_data.get("income_statement"):
                    fiscal_date = statement.pop("fiscal_date")
                    financial_objs.append(
                        StockFinancial(
                            fiscal_date=fiscal_date,
                            stock_id=id,
                            period=income_period,
                            data=statement,
                            statement=FinancialType.INCOME_STATEMENT,
                        )
                    )
            print("Storing Financials for ", stock, num_calls)
            StockFinancial.objects.bulk_create(financial_objs, ignore_conflicts=True)
        except Exception as e:
            failed_tickers_list.append(
                (stock, income_period, response_data.get("message"))
            )
            print("Failed to store data ", e, stock, num_calls)
    print(list(set(failed_tickers_list)))


def store_balancesheet():
    failed_tickers_list = []
    # Number of credits user per Call -> 100
    stock_symbol_id_map = dict(
        Stock.objects.exclude(symbol__in=invalid_ticker_symbols)
        .order_by("symbol")
        .values_list("symbol", "id")
    )

    requests_made = 0
    num_calls = 0
    financial_objs = []
    for stock, id in stock_symbol_id_map.items():
        try:
            if requests_made >= 6:
                StockFinancial.objects.bulk_create(
                    financial_objs, ignore_conflicts=True
                )
                financial_objs = []
                print("Resting for a minute .... Calls Made -> ", requests_made)
                sleep(60)
                requests_made = 0
            try:
                response = fds.get_ticker_balance_sheet(stock)
            except Exception as e:
                print("Exception", stock, e)
                failed_tickers_list.append((stock, "Network Error"))
                sleep(10)
                continue
            requests_made += 1
            num_calls += 1
            response_data = response.json()
            if not response_data.get("meta"):
                print("Error", stock, response_data.get("message"))
                failed_tickers_list.append((stock, response_data.get("message")))
                continue
            for statement in response_data.get("balance_sheet"):
                fiscal_date = statement.pop("fiscal_date")
                financial_objs.append(
                    StockFinancial(
                        fiscal_date=fiscal_date,
                        stock_id=id,
                        data=statement,
                        statement=FinancialType.BALANCE_SHEET,
                    )
                )
                print(".", end="")
        except Exception as e:
            failed_tickers_list.append((stock, response_data.get("message")))
            print("Failed to store data ", e, stock, num_calls)
    print(list(set(failed_tickers_list)))


def store_cashflow():
    failed_tickers_list = []
    # Number of credits user per Call -> 100
    stock_symbol_id_map = dict(
        Stock.objects.exclude(symbol__in=invalid_ticker_symbols)
        .order_by("symbol")
        .values_list("symbol", "id")
    )

    requests_made = 0
    num_calls = 0
    financial_objs = []
    for stock, id in stock_symbol_id_map.items():
        try:
            if requests_made >= 6:
                StockFinancial.objects.bulk_create(
                    financial_objs, ignore_conflicts=True
                )
                financial_objs = []
                print("Resting for a minute .... Calls Made -> ", requests_made)
                sleep(60)
                requests_made = 0
            try:
                response = fds.get_ticker_cash_flow(stock)
            except Exception as e:
                print("Exception", stock, e)
                failed_tickers_list.append((stock, "Network Error"))
                sleep(10)
                continue
            requests_made += 1
            num_calls += 1
            response_data = response.json()
            if not response_data.get("meta"):
                print("Error", stock, response_data.get("message"))
                failed_tickers_list.append((stock, response_data.get("message")))
                continue
            for statement in response_data.get("cash_flow"):
                fiscal_date = statement.pop("fiscal_date")
                financial_objs.append(
                    StockFinancial(
                        fiscal_date=fiscal_date,
                        stock_id=id,
                        data=statement,
                        statement=FinancialType.CASH_FLOW,
                    )
                )
                print(".", end="")
        except Exception as e:
            failed_tickers_list.append((stock, response_data.get("message")))
            print("Failed to store data ", e, stock, num_calls)
    print(list(set(failed_tickers_list)))


def store_ticker_profile():
    tds = TickerDataService()
    failed_tickers_list = []
    # Number of credits user per Call -> 10
    all_stocks = list(Stock.objects.filter())

    requests_made = 0
    num_calls = 0
    financial_objs = []
    for stock in all_stocks:
        try:
            if requests_made >= 60:
                Stock.objects.bulk_update(financial_objs, ["details"])
                financial_objs = []
                print("Resting for a minute .... Calls Made -> ", requests_made)
                sleep(60)
                requests_made = 0
            try:
                response = tds.get_ticker_profile(stock.symbol)
            except Exception as e:
                print("Exception", stock, e)
                failed_tickers_list.append((stock.symbol, "Network Error"))
                sleep(10)
                continue
            requests_made += 1
            num_calls += 1
            response_data = response.json()
            if not response_data.get("symbol").replace(".", "-") == stock.symbol:
                print("Error", stock.symbol, response_data.get("message"))
                failed_tickers_list.append((stock.symbol, response_data.get("message")))
                continue
            stock.details = {
                "employees": response_data.get("employees"),
                "website": response_data.get("website"),
                "description": response_data.get("description"),
                "type": response_data.get("type"),
                "CEO": response_data.get("CEO"),
                "phone": response_data.get("phone"),
            }

            financial_objs.append(stock)
            print(".", end="")
        except Exception as e:
            failed_tickers_list.append((stock.symbol, response_data.get("message")))
            print("Failed to store data ", e, stock.symbol, num_calls)
    if len(financial_objs) > 0:
        Stock.objects.bulk_update(financial_objs, ["details"])
    print(list(set(failed_tickers_list)))


def store_ticker_statistics():
    tds = TickerDataService()
    failed_tickers_list = []
    # Number of credits user per Call -> 10
    all_stocks = list(Stock.objects.filter())

    requests_made = 0
    num_calls = 0
    financial_objs = []
    for stock in all_stocks:
        try:
            if requests_made >= 12:
                Stock.objects.bulk_update(financial_objs, ["statistics"])
                financial_objs = []
                print("Resting for a minute .... Calls Made -> ", requests_made)
                sleep(60)
                requests_made = 0
            try:
                response = tds.get_ticker_statistics(stock.symbol)
            except Exception as e:
                print("Exception", stock, e)
                failed_tickers_list.append((stock.symbol, "Network Error"))
                sleep(10)
                continue
            requests_made += 1
            num_calls += 1
            response_data = response.json()
            if response_data.get("code", 200) != 200:
                print("Error", stock.symbol, response_data.get("message"))
                failed_tickers_list.append((stock.symbol, response_data.get("message")))
                continue
            stock.statistics = response_data.get("statistics")
            financial_objs.append(stock)
            print(".", end="")
        except Exception as e:
            failed_tickers_list.append((stock.symbol, response_data.get("message")))
            print("Failed to store data ", e, stock.symbol, num_calls)
    if len(financial_objs) > 0:
        Stock.objects.bulk_update(financial_objs, ["statistics"])
    print(list(set(failed_tickers_list)))
