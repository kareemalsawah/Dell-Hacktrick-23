"""
Riddle solvers
"""
import dpkt
import json
import socket
import base64
import numpy as np
from PIL import Image

from scapy.all import *
from io import BytesIO
#from authlib.jose import jwt
from amazoncaptcha import AmazonCaptcha
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# from authlib.jose import jwt
import base64
#import json as js
#from time import time
import jwt


new_token = {
    "alg": "RS256",
    "kty": "RSA",
    "n": "rvhfkww7G2Plzu6oceAqXabHnD5Vm5ZHAqg_Q2f6mXzyl1AUP8SlzfVRKZDfxJvPKQ8fbONQhCoU4RSKdf8pXL0MG-Q5sh45E5dhOWvLQgb6Dbtb8EBLrpSmUowY39Vpx8MR-52fK3nBhNzNZCKwjEUea4mbyzormNtQbEQodb5HKqn7mM8KAhod8-4sh3cFi01320Atox-Ud1hhtj_WWGmXEHUKlODO5cPWFMXzI2w6cqxZJ6JMNLn0Z5hppyKquUtgQf2Vzl0HFEPsgF-RjyCUfXQ_GRF4dBP6tztqrYzFGcLZ2hqZLlg0ibSsGQOHHG1bx5dezaAGkhDRm-1uIQ",
    "e": "AQAB",
    "d": "ESHOseZDr1XjvZROt_-8Bjl7WAged8KKJ29z6lS3C-pZEonLwcaueXEoxkoiLu0Wpq2NZSsIyjgYnUVWnWEjmqoEEoMRRyiAbDOpWGb-mvN17nxG70pMXsa9Vl3TXa9W0TF_hESVvjsIwMqh7ckbwlBOPzdVItwKQshOops13vld8DvPNzmkbBL2Pnp7T39D0WSaaekiqJAo-xCDzGKvBNk7PDD8i7B4BWM-ptFYK4DCN0s2oxEQ1Qz-m0yPvRJ3luUytLxC0JSYDhirqZoOOgNYqWVKn4PU1oXC6rg1nT0qvHyeQJ738eJDer1Un3R-l7qEhjRjtwfv2RCtQqeqwQ",
    "p": "6vmokKL9KghbVn0dbRQ0qYG1NbelK85ZqFgx3VnqkqqL2Iqb5Olp3ZN8D7kFmLEJyardPTOveKTb_2RlJuFg-OTSyPlAKnTewIlT9o28S3BZ9gsmjTnoiarkDlmvz2AxViGAMeo3HoIxtTHVb70J7_shClhr1ZQFNH4LAxh_vEk",
    "q": "vqA9evTUANwMeuPRHYVtjVwy0MeWhC1OI4aJOGgK7PfcELpCmPn5uhLrBQeJBVGsnWFDpHWJRVXJyMxW2EUhS1PmrKuE0-DWYElnA57fHy5PyZ9EFGC3swznQjzyZnbvezDvhvmdKdAql48NlAPYKEFyxA-WYB4NSAt25K5lsxk",
    "dp": "m_tpU8JuzqVHhM1_aDaektug4Gztf3v29pK9X1ReLEh8lx3ESRxNg6JxG7rWJTt45N_BB-y0kiDWTd5ma333sqGr72_OkaCNckB3dVc3ZNjLT1Ktn9iOLj08MO6Gj-IqPiP1Bq2VM3J37vGK3ycdXqpVj5mM0_Xz0pnNU5vCx8k",
    "dq": "vK4WrHFQtlkX8Ts1bKb4vIaZtZUYIlRFl1w-zhoNVmgu5k-2Q3yJ9edrwFqpAR7KYCw5q7q62GoFhD7dZstmHQ06sYZDvwQ4rK16zVafOlm4l7SQyirBKPSIokN5Gnp2p9TUASFosk5dGg56PhtgBNhjJDTZfuG_-6N9VvRXrWE",
    "qi": "OCujpxTMOSQzbsBTPAnH1vyagaSMsYt_FHNSTfLfw1qkE9TAi2eZM2XOzFl74RkGsHkfwNmFaLBC8rtZRLg0hWZAMrdH7NYHcHQCSxQtSspLVgPuiRBtccHEPzX-4C_rXxwPxhrF0XVKkixANzTUOb1IwSqkYyDDoal-mY7-7RM",
}


# Generate or load private key
if os.path.exists("private_key.pem"):
    #t2 = time()
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
else:
    private_key = jwt.algorithms.RSAAlgorithm.from_jwk(new_token)
    with open("private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def server_solver(question):

    # split the question into parts by .
    parts = question.split(".")
    header = base64.b64decode(parts[0] + "=" * (-len(parts[0]) % 4))
    payload = base64.b64decode(parts[1] + "=" * (-len(parts[1]) % 4))
    header = json.loads(header)
    payload = json.loads(payload)

    # change the header and payload
    payload["admin"] = "true"
    header["jwk"]["e"] = new_token["e"]
    header["jwk"]["n"] = new_token["n"]

    # encode the new header and payload using the new jwk token that includes the private key
    # token = jwt.encode(header, payload, new_token).decode("utf-8")
    token = jwt.encode(
        headers=header, payload=payload, key=private_key, algorithm="RS256"
    )
    return token


# don't forget to have a temp image named "img.png"
def captcha_solver(img_data: str) -> str:
    captcha = AmazonCaptcha("./img.png")
    captcha.img = Image.fromarray(np.array(img_data).astype(np.uint8))
    return captcha.solve()


def pcap_solver(pcap_str: str) -> str:
    pcap = base64.b64decode(pcap_str + "=" * (-len(pcap_str) % 4))

    # Assuming pcap_data contains the byte object of the pcap file
    pcap = dpkt.pcap.Reader(BytesIO(pcap))

    words = [""] * 100000

    # Loop over packets and do something with them
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        # Check if destination IP address matches 188.68.45.12 and protocol is DNS
        if (
            isinstance(ip, dpkt.ip.IP)
            and ip.dst == socket.inet_aton("188.68.45.12")
            and ip.p == dpkt.ip.IP_PROTO_UDP
        ):
            udp = ip.data
            # Check if packet is a DNS query
            if udp.sport == 53:
                dns = dpkt.dns.DNS(udp.data)
                # Get the list of question records
                qd_list = dns.qd
                # Loop over question records and print the name of each one
                for i in range(len(qd_list)):
                    info = qd_list[i].name.split(".")[0:2]
                    position = int(
                        base64.b64decode(info[0] + "=" * (-len(info[0]) % 4)).decode(
                            "utf-8"
                        )
                    )
                    words[position - 1] = base64.b64decode(
                        info[1] + "=" * (-len(info[1]) % 4)
                    ).decode("utf-8")

    secret = "".join(words)
    return secret


def caesar_decrypt(ciphertext, key):
    plaintext = ""
    for char in ciphertext:
        # Check if the character is a letter
        if char.isalpha():
            # Determine the case of the letter
            if char.isupper():
                case = "upper"
            else:
                case = "lower"
            # Convert the letter to its corresponding ASCII code
            code = ord(char)
            # Shift the code by the key value
            code -= key
            # Wrap around if necessary
            if case == "upper" and code < ord("A"):
                code += 26
            elif case == "lower" and code < ord("a"):
                code += 26
            # Convert the ASCII code back to a letter and add to the plaintext
            plaintext += chr(code)
        else:
            plaintext += char
    return plaintext


def cipher_solver(question):
    binary = base64.b64decode(question + "=" * (-len(question) % 4))[1:-1].split(b",")
    text = binary[0]
    shift = int(binary[1], 2)
    text_padded = b""

    for i in range(0, len(text), 7):
        text_padded += b"0"
        text_padded += text[i : i + 7]

    text_padded = int(text_padded, 2)

    Total_bytes = (text_padded.bit_length() + 7) // 8

    input_array = text_padded.to_bytes(Total_bytes, "big")
    ASCII_value = input_array.decode()

    return caesar_decrypt(ASCII_value, shift)
