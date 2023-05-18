import logging
from typing import Any

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


def show(*args, **kwargs):
    print(*args, *kwargs.values(), sep='\n')


def new_totp():
    pw = totp.now()
    logging.debug(f'{pw}')
    return pw


def get_otp_uri(name: str = '', title: str = ''):
    name = name or 'OTP@EXAMPLE.COM'
    title = title or 'Secure App'
    logging.debug(f'{name=}, {title=}')
    logging.debug(
        uri := (
            pyotp.totp.TOTP(SECRET_KEY)
            .provisioning_uri(name=name, issuer_name=title)
        )
    )
    return uri


def tratativa0(qr_code: Any) -> Any:
    """Tratativa em manipular o qr resultante."""
    # Fail
    stream0 = BytesIO(qr_code.print_ascii())
    logging.debug(stream0)
    return stream0


def tratativa1(qr_code: Any) -> Any:
    """Tratativa em manipular o qr resultante."""
    output = Path(NamedTemporaryFile(suffix='.png', prefix='qr_').name)
    qr_code.save(output.as_posix())
    with output.open('rb') as f:
        stream1 = BytesIO(f.read())
    logging.debug(stream1)
    return stream1


def tratativa2(uri: str = '') -> Any:
    """Tratativa em manipular o qr resultante."""
    qr_code = qrcode.QRCode()
    qr_code.add_data(uri)

    with StringIO() as file:
        qr_code.print_ascii(out=file)
        file.seek(0)
        stream = file.read()
    logging.debug(type(stream))
    return stream


def run():
    # OTP verified for current time
    show(
        pw := new_totp(),
        totp.verify(pw),  # => True
        time.sleep(30),
        totp.verify(pw),  # => False
        get_otp_uri()
    )

    qr = qrcode.make(get_otp_uri())
    show(
        # tratativa0(qr),
        '---',
        tratativa1(qr),
        '---',
        tratativa2(get_otp_uri())
    )


if __name__ == '__main__':
    run()
