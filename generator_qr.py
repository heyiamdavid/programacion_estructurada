import qrcode

texto = "https://github.com/heyiamdavid/programacion_estructurada"

qr = qrcode.QRCode(version=1,
                    box_size=10,
                    border=2)
qr.add_data(texto)
qr.make(fit=True)

imagen_qr = qr.make_image(fill_color="black",
                          back_color="white")
imagen_qr.save("qr_image/codigo_qr.png")                          
