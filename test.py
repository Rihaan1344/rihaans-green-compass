import qrcode

data = "https://example.com"

qr = qrcode.make(data)
qr.save("qrcode.png")