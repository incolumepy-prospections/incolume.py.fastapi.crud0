import pyotp
import time
import qrcode
from tempfile import gettempdir, NamedTemporaryFile
from pathlib import Path
from io import BytesIO, StringIO

secrets_keys = [pyotp.random_base32(), pyotp.random_hex()]

print(secrets_keys)
secret_key = 'JBSWY3DPEHPK3PXP'

totp = pyotp.totp.TOTP(secret_key)

pw = totp.now()

# OTP verified for current time
print(
    pw,
    totp.verify(pw),  # => True
    time.sleep(30),
    totp.verify(pw),  # => False
    uri :=
    pyotp.totp.TOTP(secret_key).provisioning_uri(name='ops@example.com',
                                                 issuer_name='Secure App'),
    sep='\n')

qr = qrcode.make(uri)
# stream0 = BytesIO(qr.get_image())

output = Path(NamedTemporaryFile(suffix='.png', prefix='qr_').name)

qr.save(output.as_posix())

with output.open('rb') as f:
    stream1 = BytesIO(f.read())

qr2 = qrcode.QRCode()
qr2.add_data(uri)

with StringIO() as f:
    qr2.print_ascii(out=f)
    f.seek(0)
    stream2 = f.read()

print(
    # f'{type(stream0)}: {stream0}',
    f'{type(qr)}: {qr}',
    f'{output.exists()}: {output.as_posix()}',
    f'{qr.get_image()=}',
    f'{type(stream1)}: {stream1}',
    dir(qr.get_image()),
    f'{type(stream2)}: {stream2=}',
    sep='\n' * 2)
