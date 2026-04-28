import qrcode

data = "https://banyantreeactivity.tiiny.site/"

qr = qrcode.make(data)
qr.save("qrcode.png")