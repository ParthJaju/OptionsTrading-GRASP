import re
import time
import struct
import socket
from django.core.management.base import BaseCommand
from datetime import datetime

from chains.models import Option, OptionPrice
from chains.views import extract_symbol_components

# Packet length 
PACKET_LENGTH_OFFSET = 0
PACKET_LENGTH_SIZE = 4

# Trading symbol 
SYMBOL_OFFSET = 4 
SYMBOL_SIZE = 30

# Sequence number 
SEQ_NUM_OFFSET = 34
SEQ_NUM_SIZE = 8

# Timestamp 
TIMESTAMP_OFFSET = 42
TIMESTAMP_SIZE = 8

# Last traded price 
LTP_OFFSET = 50
LTP_SIZE = 8

# Last traded quantity
LTQ_OFFSET = 58
LTQ_SIZE = 8

# Volume
VOLUME_OFFSET = 66 
VOLUME_SIZE = 8

# Bid price 
BID_PRICE_OFFSET = 74
BID_PRICE_SIZE = 8

# Bid quantity
BID_QTY_OFFSET = 82
BID_QTY_SIZE = 8

# Ask price
ASK_PRICE_OFFSET = 90
ASK_PRICE_SIZE = 8

# Ask quantity 
ASK_QTY_OFFSET = 98
ASK_QTY_SIZE = 8

# Open interest
OI_OFFSET = 106
OI_SIZE = 8

# Previous close price
PREV_CLOSE_OFFSET = 114
PREV_CLOSE_SIZE = 8

# Previous OI
PREV_OI_OFFSET = 122
PREV_OI_SIZE = 8

class Command(BaseCommand):
    def handle(self, *args, **options):
        host = 'localhost'
        port = 9011

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        while True:
            client_socket.send(b'1')  
            # Receive 130 byte market data packet 
            try:
                data = client_socket.recv(130)  
                print('Receiving from server', host, port)
                # Unpack fields
                packet_length = struct.unpack('<i', data[PACKET_LENGTH_OFFSET:PACKET_LENGTH_OFFSET + PACKET_LENGTH_SIZE])[0]
                symbol = struct.unpack('<30s', data[SYMBOL_OFFSET:SYMBOL_OFFSET + SYMBOL_SIZE])[0].decode().strip('\x00')
                seq_num = struct.unpack('<q', data[SEQ_NUM_OFFSET:SEQ_NUM_OFFSET + SEQ_NUM_SIZE])[0]
                timestamp = struct.unpack('<q', data[TIMESTAMP_OFFSET:TIMESTAMP_OFFSET + TIMESTAMP_SIZE])[0]
                ltp = struct.unpack(f'<q', data[LTP_OFFSET:LTP_OFFSET + LTP_SIZE])[0] / 100
                ltq = struct.unpack('<q', data[LTQ_OFFSET:LTQ_OFFSET + LTQ_SIZE])[0]
                volume = struct.unpack('<q', data[VOLUME_OFFSET:VOLUME_OFFSET + VOLUME_SIZE])[0]
                bid_price = struct.unpack('<q', data[BID_PRICE_OFFSET:BID_PRICE_OFFSET + BID_PRICE_SIZE])[0] / 100
                bid_qty = struct.unpack('<q', data[BID_QTY_OFFSET:BID_QTY_OFFSET + BID_QTY_SIZE])[0]
                ask_price = struct.unpack('<q', data[ASK_PRICE_OFFSET:ASK_PRICE_OFFSET + ASK_PRICE_SIZE])[0] / 100
                ask_qty = struct.unpack('<q', data[ASK_QTY_OFFSET:ASK_QTY_OFFSET + ASK_QTY_SIZE])[0]  
                oi = struct.unpack('<q', data[OI_OFFSET:OI_OFFSET + OI_SIZE])[0]
                prev_close = struct.unpack('<q', data[PREV_CLOSE_OFFSET:PREV_CLOSE_OFFSET + PREV_CLOSE_SIZE])[0] / 100
                prev_oi = struct.unpack('<q', data[PREV_OI_OFFSET:PREV_OI_OFFSET + PREV_OI_SIZE])[0]

                # Construct market data object
                market_data = {
                    'packet_length': packet_length,
                    'symbol': symbol, 
                    'seq_num': seq_num,
                    'timestamp': timestamp,
                    'ltp': ltp,
                    'ltq': ltq,
                    'volume': volume,
                    'bid_price': bid_price,
                    'bid_qty': bid_qty,
                    'ask_price': ask_price,
                    'ask_qty': ask_qty,
                    'oi': oi,
                    'prev_close': prev_close,
                    'prev_oi': prev_oi
                }
                timestamp = datetime.fromtimestamp(timestamp/1000)
                ltp = float(ltp)
                ltq = int(ltq)
                volume = int(volume)
                bid_price = float(bid_price)
                bid_qty = int(bid_qty)
                ask_price = float(ask_price)
                ask_qty = int(ask_qty)
                oi = int(oi)
                prev_close = float(prev_close)
                prev_oi = int(prev_oi)
                name, expiry, strike_price, put_call = extract_symbol_components(symbol)
                if expiry:
                    expiry = datetime.strptime(expiry, '%d %b %y').date()
                price = 0.0
                if strike_price:
                    price = float(strike_price)
                option = Option.objects.filter(symbol=name, expiration=expiry, strike_price=price, option_type=put_call).first()
                if option:
                    option_price = OptionPrice.objects.filter(option_id=option.id)
                    if option_price:
                            option_price.update(
                                ltp=ltp,
                                ltq=ltq,
                                volume=volume,
                                bid_price=bid_price,
                                bid_qty=bid_qty,
                                ask_price=ask_price,
                                ask_qty=ask_qty,
                                oi=oi,
                                streamtime=timestamp
                            )
                    else:
                        option_price = OptionPrice.objects.create(
                            option=option,
                            ltp=ltp,
                            ltq=ltq,
                            volume=volume,
                            bid_price=bid_price,
                            bid_qty=bid_qty,
                            ask_price=ask_price,
                            ask_qty=ask_qty,
                            oi=oi,
                            streamtime=timestamp
                        )
                print(market_data)
            except:
                pass
       
