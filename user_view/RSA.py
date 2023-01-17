import rsa


def decode_PCKE(PCKE):

    with open("user_view/privat.pem", "rb") as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())

    PCKE_de = rsa.decrypt(PCKE, private_key)

    return PCKE_de.decode()