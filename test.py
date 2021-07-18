import gnupg
import pprint


gpg = gnupg.GPG()
gpg.encoding = 'utf8'

message = """
-----BEGIN PGP MESSAGE-----

hQIMA9O7n1YjUQuPAQ/9HYi5NBkgfNRsVJm+jb4JWOGaslIcsCmgD5sPo0daJStQ
B5iJaxdCQXT+nCqCcVj9E+HUMSGVyFenXRuT39Z1ew84s+LMIONW9r3I7w/TmB5y
oKCgVQNrMl8W/qhRkJtW9bJYqwy0EaSCNBi9lc5kGhAUmfe4zeSTHYthkqdYrMGd
MaE5WGHpgPXP1FKvduA5tpEjXrj8LCWSG+QtrIFDJaP/1b3dBlZ9JXg87H4gPtA+
rb5Sp+qcGWevd869yJYHFgumVoOpqzuwim6LuY35htjX2ge8uv2w4D2/lsvWhNc2
e5GeA7UyEYrWl0neHAJcjseB6IA47uhQ3lbPpq1l1ZXsdUj5yYzwe9mCGbLDtP6V
kzHAAuPr6X/fUGzSuDj5H/LU5ryptj+RFqZ9as3r4eOaCLvhGMAtPjxJV+ZbfDTi
5vOBpk9ScQPEqLQwsvf741B8hMSZ3FiRKm5LtBfNzwoK0/1Z6zssb+T3AnEpiPAV
390z8R0rrnU4Sjm9d//gpQRg0OYfx+s0rHXUbC/cYNWCXhtjXJdoF3WORIoV4uXG
4JkqxTiNG7fIXHECsFGNkmH4MfEvhh9P8+LlXniejf0FzlBaU4uX3jN5klbBBz1A
kQk48KiNzXLDTrh3whKP0i8sQ6Z5y8m2VQFxLNoI97e9h6j2FeMWlktsLuwScITS
wMsB/MQLehms9Apds9J5CwFByFJWWCJi6EICRHCZihxh8Ki/AzTCUhMEzdZvAufY
3o3MQH44m5LQuGb9JonI82AHsz7WfXIV92RfE26lqRyrX3+HLYzfHH7E35lSETId
T9t5PyS/uV7kaOa2G9bQ8rj6qk/ZCVxLl18OV0qHTh5ppTStVfzutYjcevjHcLEj
VhJjqgwwoSOmzhsp0kghCz1N9FpuJ5OhPUm5duCSc4f42psvrrB5ZuP5/ynAEyIR
kGZMj/H8ii+8kHDXG8ppTxPufosHaIV5ZDu+HQipF/U17Xsyavgj+0CZImt9q1Z7
B8iRl/ZolF/sB52VggvHDGHWBUM36JjOWgYUzPkqjSnKMdjERGcBav12ik5JbfI8
5BZpmuGl7ZeW6h5I74i3RcmOdZNiKL80emaZvn1EIS8lXb3FI8hq7AsWD496TGE5
7NQLgXLj0ccNl66DkTYRkDj4JQE0UsRSfjyQLdBSyCmIgFoRxSk0DAdrplXVPWm1
qwshuZkZ3w/SHBo02A==
=8H70
-----END PGP MESSAGE-----

"""
decrypted_data = gpg.decrypt(message)
print(decrypted_data)

my_printer = pprint.PrettyPrinter(depth=3)

public_keys = gpg.list_keys()

for key in public_keys:
    print("".join(key['uids']))
    print(key['fingerprint'])

ascii_data = "test deneme"
recipients = ['9D184AC865E2CD0B40C5B5D2D95479E839D351FD']
encrypted_ascii_data = gpg.encrypt(ascii_data, recipients)
print(encrypted_ascii_data)