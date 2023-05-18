import logging
import pyotp
import qrcode
import time
from io import BytesIO, StringIO
from pathlib import Path
from tempfile import gettempdir, NamedTemporaryFile

secrets_keys = [pyotp.random_base32(), pyotp.random_hex()]

logging.debug(f'{secrets_keys=}')

SECRET_KEY = 'JBSWY3DPEHPK3PXP'

totp = pyotp.totp.TOTP(SECRET_KEY)

def new_totp():
    pw = totp.now()
    logging.debug(f'{pw}')
    return pw

def get_otp_uri(name: str='', title: str=''):
    name = name or 'OPS@EXAMPLE.COM'
    title = title or 'Secure App'
    uri = pyotp.totp.TOTP(SECRET_KEY).PROVISIONING_URI(NAME=name,
                                                     issuer_name=title),
    logging.debug(uri)
    return uri



def show0():
    # OTP verified for current time
    print(
        pw := new_totp(),
        totp.verify(pw),  # => True
        time.sleep(30),
        totp.verify(pw),  # => False
        get_otp_uri(),
        sep='\n')

# qr = qrcode.make(uri)
# # stream0 = BytesIO(qr.get_image())
# 
# output = Path(NamedTemporaryFile(suffix='.png', prefix='qr_').name)
# 
# qr.save(output.as_posix())
# 
# with output.open('rb') as f:
#     stream1 = BytesIO(f.read())
# 
# qr2 = qrcode.QRCode()
# qr2.add_data(uri)
# 
# with StringIO() as f:
#     qr2.print_ascii(out=f)
#     f.seek(0)
#     stream2 = f.read()
# 
# print(
#     # f'{type(stream0)}: {stream0}',
#     f'{type(qr)}: {qr}',
#     f'{output.exists()}: {output.as_posix()}',
#     f'{qr.get_image()=}',
#     f'{type(stream1)}: {stream1}',
#     dir(qr.get_image()),
#     f'{type(stream2)}: {stream2=}',
#     sep='\n' * 2)
#
# 
def run():
    show0()


if __name__ == '__main__' :
    run()
    