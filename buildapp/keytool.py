import datetime
from pathlib import Path

from cryptography.x509.name import Name, NameOID, NameAttribute
from cryptography.x509.extensions import SubjectAlternativeName
from cryptography.x509 import CertificateBuilder, random_serial_number, DNSName

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption


def generate_keypair_keystore(keystore_path: Path): # TODO: keystore_alias: str, keystore_pass: str
    KEY_SIZE = 2048
    RSA_PUBLIC_EXPONENT = 65537

    private_key = rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT,
        key_size=KEY_SIZE,
        backend=default_backend()
    )

    subject = issuer = Name([
        NameAttribute(NameOID.COUNTRY_NAME, u'US'),
        NameAttribute(NameOID.COMMON_NAME, u'localhost'),
        NameAttribute(NameOID.ORGANIZATION_NAME, u'MyOrganization')
    ])

    KEY_ALG = "RSA"
    VALIDITY_DAYS = 10000
    cert = CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(private_key.public_key()
    ).serial_number(
        random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=VALIDITY_DAYS)
    ).add_extension(
        SubjectAlternativeName([DNSName(u"localhost")]),
        critical=False,
    ).sign(private_key, SHA256(), default_backend())

    with open(keystore_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        ))

        f.write(cert.public_bytes(Encoding.PEM))
