# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.precise import Precise


class indodax(Exchange):

    def describe(self):
        return self.deep_extend(super(indodax, self).describe(), {
            'id': 'indodax',
            'name': 'INDODAX',
            'countries': ['ID'],  # Indonesia
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'createMarketOrder': None,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchClosedOrders': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchIsolatedPositions': False,
                'fetchLeverage': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': None,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': None,
                'fetchPosition': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': None,
                'fetchTime': True,
                'fetchTrades': True,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
                'withdraw': True,
            },
            'version': '2.0',  # as of 9 April 2018
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87070508-9358c880-c221-11ea-8dc5-5391afbbb422.jpg',
                'api': {
                    'public': 'https://indodax.com/api',
                    'private': 'https://indodax.com/tapi',
                },
                'www': 'https://www.indodax.com',
                'doc': 'https://github.com/btcid/indodax-official-api-docs',
                'referral': 'https://indodax.com/ref/testbitcoincoid/1',
            },
            'api': {
                'public': {
                    'get': [
                        'server_time',
                        'pairs',
                        '{pair}/ticker',
                        '{pair}/trades',
                        '{pair}/depth',
                    ],
                },
                'private': {
                    'post': [
                        'getInfo',
                        'transHistory',
                        'trade',
                        'tradeHistory',
                        'getOrder',
                        'openOrders',
                        'cancelOrder',
                        'orderHistory',
                        'withdrawCoin',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0,
                    'taker': 0.003,
                },
            },
            'exceptions': {
                'exact': {
                    'invalid_pair': BadSymbol,  # {"error":"invalid_pair","error_description":"Invalid Pair"}
                    'Insufficient balance.': InsufficientFunds,
                    'invalid order.': OrderNotFound,
                    'Invalid credentials. API not found or session has expired.': AuthenticationError,
                    'Invalid credentials. Bad sign.': AuthenticationError,
                },
                'broad': {
                    'Minimum price': InvalidOrder,
                    'Minimum order': InvalidOrder,
                },
            },
            # exchange-specific options
            'options': {
                'recvWindow': 5 * 1000,  # default 5 sec
                'timeDifference': 0,  # the difference between system clock and exchange clock
                'adjustForTimeDifference': False,  # controls the adjustment logic upon instantiation
            },
            'commonCurrencies': {
                'STR': 'XLM',
                'BCHABC': 'BCH',
                'BCHSV': 'BSV',
                'DRK': 'DASH',
                'NEM': 'XEM',
            },
        })

    def nonce(self):
        return self.milliseconds() - self.options['timeDifference']

    async def fetch_time(self, params={}):
        response = await self.publicGetServerTime(params)
        #
        #     {
        #         "timezone": "UTC",
        #         "server_time": 1571205969552
        #     }
        #
        return self.safe_integer(response, 'server_time')

    async def fetch_markets(self, params={}):
        response = await self.publicGetPairs(params)
        #
        #     [
        #         {
        #             "id": "btcidr",
        #             "symbol": "BTCIDR",
        #             "base_currency": "idr",
        #             "traded_currency": "btc",
        #             "traded_currency_unit": "BTC",
        #             "description": "BTC/IDR",
        #             "ticker_id": "btc_idr",
        #             "volume_precision": 0,
        #             "price_precision": 1000,
        #             "price_round": 8,
        #             "pricescale": 1000,
        #             "trade_min_base_currency": 10000,
        #             "trade_min_traded_currency": 0.00007457,
        #             "has_memo": False,
        #             "memo_name": False,
        #             "has_payment_id": False,
        #             "trade_fee_percent": 0.3,
        #             "url_logo": "https://indodax.com/v2/logo/svg/color/btc.svg",
        #             "url_logo_png": "https://indodax.com/v2/logo/png/color/btc.png",
        #             "is_maintenance": 0
        #         }
        #     ]
        #
        result = []
        for i in range(0, len(response)):
            market = response[i]
            id = self.safe_string(market, 'ticker_id')
            baseId = self.safe_string(market, 'traded_currency')
            quoteId = self.safe_string(market, 'base_currency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            isMaintenance = self.safe_integer(market, 'is_maintenance')
            result.append({
                'id': id,
                'symbol': base + '/' + quote,
                'base': base,
                'quote': quote,
                'settle': None,
                'baseId': baseId,
                'quoteId': quoteId,
                'settleId': None,
                'type': 'spot',
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'active': False if isMaintenance else True,
                'contract': False,
                'linear': None,
                'inverse': None,
                'taker': self.safe_number(market, 'trade_fee_percent'),
                'contractSize': None,
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'percentage': True,
                'precision': {
                    'amount': int('8'),
                    'price': self.safe_integer(market, 'price_round'),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': self.safe_number(market, 'trade_min_traded_currency'),
                        'max': None,
                    },
                    'price': {
                        'min': self.safe_number(market, 'trade_min_base_currency'),
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def parse_balance(self, response):
        balances = self.safe_value(response, 'return', {})
        free = self.safe_value(balances, 'balance', {})
        used = self.safe_value(balances, 'balance_hold', {})
        timestamp = self.safe_timestamp(balances, 'server_time')
        result = {
            'info': response,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
        }
        currencyIds = list(free.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(free, currencyId)
            account['used'] = self.safe_string(used, currencyId)
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostGetInfo(params)
        #
        #     {
        #         "success":1,
        #         "return":{
        #             "server_time":1619562628,
        #             "balance":{
        #                 "idr":167,
        #                 "btc":"0.00000000",
        #                 "1inch":"0.00000000",
        #             },
        #             "balance_hold":{
        #                 "idr":0,
        #                 "btc":"0.00000000",
        #                 "1inch":"0.00000000",
        #             },
        #             "address":{
        #                 "btc":"1KMntgzvU7iTSgMBWc11nVuJjAyfW3qJyk",
        #                 "1inch":"0x1106c8bb3172625e1f411c221be49161dac19355",
        #                 "xrp":"rwWr7KUZ3ZFwzgaDGjKBysADByzxvohQ3C",
        #                 "zrx":"0x1106c8bb3172625e1f411c221be49161dac19355"
        #             },
        #             "user_id":"276011",
        #             "name":"",
        #             "email":"testbitcoincoid@mailforspam.com",
        #             "profile_picture":null,
        #             "verification_status":"unverified",
        #             "gauth_enable":true
        #         }
        #     }
        #
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        orderbook = await self.publicGetPairDepth(self.extend(request, params))
        return self.parse_order_book(orderbook, symbol, None, 'buy', 'sell')

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "high":"0.01951",
        #         "low":"0.01877",
        #         "vol_eth":"39.38839319",
        #         "vol_btc":"0.75320886",
        #         "last":"0.01896",
        #         "buy":"0.01896",
        #         "sell":"0.019",
        #         "server_time":1565248908
        #     }
        #
        symbol = self.safe_symbol(None, market)
        timestamp = self.safe_timestamp(ticker, 'server_time')
        baseVolume = 'vol_' + market['baseId'].lower()
        quoteVolume = 'vol_' + market['quoteId'].lower()
        last = self.safe_string(ticker, 'last')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high'),
            'low': self.safe_string(ticker, 'low'),
            'bid': self.safe_string(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_string(ticker, baseVolume),
            'quoteVolume': self.safe_string(ticker, quoteVolume),
            'info': ticker,
        }, market, False)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = await self.publicGetPairTicker(self.extend(request, params))
        #
        #     {
        #         "ticker": {
        #             "high":"0.01951",
        #             "low":"0.01877",
        #             "vol_eth":"39.38839319",
        #             "vol_btc":"0.75320886",
        #             "last":"0.01896",
        #             "buy":"0.01896",
        #             "sell":"0.019",
        #             "server_time":1565248908
        #         }
        #     }
        #
        ticker = self.safe_value(response, 'ticker', {})
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'date')
        id = self.safe_string(trade, 'tid')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        type = None
        side = self.safe_string(trade, 'type')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'order': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = await self.publicGetPairTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            'open': 'open',
            'filled': 'closed',
            'cancelled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "order_id": "12345",
        #         "submit_time": "1392228122",
        #         "price": "8000000",
        #         "type": "sell",
        #         "order_ltc": "100000000",
        #         "remain_ltc": "100000000"
        #     }
        #
        # market closed orders - note that the price is very high
        # and does not reflect actual price the order executed at
        #
        #     {
        #       "order_id": "49326856",
        #       "type": "sell",
        #       "price": "1000000000",
        #       "submit_time": "1618314671",
        #       "finish_time": "1618314671",
        #       "status": "filled",
        #       "order_xrp": "30.45000000",
        #       "remain_xrp": "0.00000000"
        #     }
        side = None
        if 'type' in order:
            side = order['type']
        status = self.parse_order_status(self.safe_string(order, 'status', 'open'))
        symbol = None
        cost = None
        price = self.safe_string(order, 'price')
        amount = None
        remaining = None
        if market is not None:
            symbol = market['symbol']
            quoteId = market['quoteId']
            baseId = market['baseId']
            if (market['quoteId'] == 'idr') and ('order_rp' in order):
                quoteId = 'rp'
            if (market['baseId'] == 'idr') and ('remain_rp' in order):
                baseId = 'rp'
            cost = self.safe_string(order, 'order_' + quoteId)
            if not cost:
                amount = self.safe_string(order, 'order_' + baseId)
                remaining = self.safe_string(order, 'remain_' + baseId)
        timestamp = self.safe_integer(order, 'submit_time')
        fee = None
        id = self.safe_string(order, 'order_id')
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': 'limit',
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'cost': cost,
            'average': None,
            'amount': amount,
            'filled': None,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': None,
        })

    async def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'order_id': id,
        }
        response = await self.privatePostGetOrder(self.extend(request, params))
        orders = response['return']
        order = self.parse_order(self.extend({'id': id}, orders['order']), market)
        return self.extend({'info': response}, order)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = await self.privatePostOpenOrders(self.extend(request, params))
        rawOrders = response['return']['orders']
        # {success: 1, return: {orders: null}} if no orders
        if not rawOrders:
            return []
        # {success: 1, return: {orders: [... objects]}} for orders fetched by symbol
        if symbol is not None:
            return self.parse_orders(rawOrders, market, since, limit)
        # {success: 1, return: {orders: {marketid: [... objects]}}} if all orders are fetched
        marketIds = list(rawOrders.keys())
        exchangeOrders = []
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            marketOrders = rawOrders[marketId]
            market = self.markets_by_id[marketId]
            parsedOrders = self.parse_orders(marketOrders, market, since, limit)
            exchangeOrders = self.array_concat(exchangeOrders, parsedOrders)
        return exchangeOrders

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        await self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = await self.privatePostOrderHistory(self.extend(request, params))
        orders = self.parse_orders(response['return']['orders'], market)
        orders = self.filter_by(orders, 'status', 'closed')
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'type': side,
            'price': price,
        }
        currency = market['baseId']
        if side == 'buy':
            request[market['quoteId']] = amount * price
        else:
            request[market['baseId']] = amount
        request[currency] = amount
        result = await self.privatePostTrade(self.extend(request, params))
        data = self.safe_value(result, 'return', {})
        id = self.safe_string(data, 'order_id')
        return {
            'info': result,
            'id': id,
        }

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol argument')
        side = self.safe_value(params, 'side')
        if side is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires an extra "side" param')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'pair': market['id'],
            'type': side,
        }
        return await self.privatePostCancelOrder(self.extend(request, params))

    async def withdraw(self, code, amount, address, tag=None, params={}):
        tag, params = self.handle_withdraw_tag_and_params(tag, params)
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        # Custom string you need to provide to identify each withdrawal.
        # Will be passed to callback URL(assigned via website to the API key)
        # so your system can identify the request and confirm it.
        # Alphanumeric, max length 255.
        requestId = self.milliseconds()
        # Alternatively:
        # requestId = self.uuid()
        request = {
            'currency': currency['id'],
            'withdraw_amount': amount,
            'withdraw_address': address,
            'request_id': str(requestId),
        }
        if tag:
            request['withdraw_memo'] = tag
        response = await self.privatePostWithdrawCoin(self.extend(request, params))
        #
        #     {
        #         "success": 1,
        #         "status": "approved",
        #         "withdraw_currency": "xrp",
        #         "withdraw_address": "rwWr7KUZ3ZFwzgaDGjKBysADByzxvohQ3C",
        #         "withdraw_amount": "10000.00000000",
        #         "fee": "2.00000000",
        #         "amount_after_fee": "9998.00000000",
        #         "submit_time": "1509469200",
        #         "withdraw_id": "xrp-12345",
        #         "txid": "",
        #         "withdraw_memo": "123123"
        #     }
        #
        id = None
        if ('txid' in response) and (len(response['txid']) > 0):
            id = response['txid']
        return {
            'info': response,
            'id': id,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            url += '/' + self.implode_params(path, params)
        else:
            self.check_required_credentials()
            body = self.urlencode(self.extend({
                'method': path,
                'timestamp': self.nonce(),
                'recvWindow': self.options['recvWindow'],
            }, params))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        # {success: 0, error: "invalid order."}
        # or
        # [{data, ...}, {...}, ...]
        if isinstance(response, list):
            return  # public endpoints may return []-arrays
        error = self.safe_value(response, 'error', '')
        if not ('success' in response) and error == '':
            return  # no 'success' property on public responses
        if self.safe_integer(response, 'success', 0) == 1:
            # {success: 1, return: {orders: []}}
            if not ('return' in response):
                raise ExchangeError(self.id + ': malformed response: ' + self.json(response))
            else:
                return
        feedback = self.id + ' ' + body
        self.throw_exactly_matched_exception(self.exceptions['exact'], error, feedback)
        self.throw_broadly_matched_exception(self.exceptions['broad'], error, feedback)
        raise ExchangeError(feedback)  # unknown message
