import flet as ft
import qrcode
import io
import os
import base64
import platform
import subprocess
import threading
import time

def main(page: ft.Page):
    page.title = "Generador de QR"
    page.window.width = 492
    page.window.height = 567
    page.window_resizable = False  # Bloquea redimensionamiento
    page.window_maximizable = False  # Opcional: desactiva botón de maximizar
    page.window_minimizable = True  # Permite minimizar si quieres
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    

    def abrir_explorador(ruta):
        carpeta = os.path.dirname(ruta)
        try:
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{carpeta}"')  # Aparece en primer plano
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", carpeta])
            else:
                subprocess.Popen(["xdg-open", carpeta])
        except Exception as ex:
            print("Error al abrir carpeta:", ex)


    def ocultar_mensaje_y_qr():
        time.sleep(20)
        success_message.visible = False
        qr_image.visible = False
        abrir_carpeta_button.visible = False
        page.update()

    def generar_qr(e):
        if link_input.value:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(link_input.value)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            
            # Guardar imagen
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            last_six_chars = link_input.value[-6:] if len(link_input.value) > 6 else link_input.value
            img_path = os.path.join(downloads_path, f"qr_code_{last_six_chars}.png")
            img.save(img_path)

            # Convertir a base64
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
            qr_image.src_base64 = img_base64
            qr_image.visible = True

            # Mostrar mensaje y botón
            success_message.value = "✅ QR generado exitosamente. Puedes abrir la carpeta:"
            success_message.visible = True
            abrir_carpeta_button.visible = True
            abrir_carpeta_button.on_click = lambda e: abrir_explorador(img_path)

            # Limpiar campo
            link_input.value = ""
            link_input.error_text = ""
            page.update()

            # Ocultar mensaje y QR después de 20 segundos
            threading.Thread(target=ocultar_mensaje_y_qr, daemon=True).start()
        else:
            link_input.error_text = "Por favor, introduce un enlace"
            page.update()

    # Componentes UI
    link_input = ft.TextField(label="Introduce el enlace", width=300)
    generar_button = ft.ElevatedButton("Generar QR", on_click=generar_qr)
    qr_image = ft.Image(width=300, height=300, visible=False)
    success_message = ft.Text("", visible=False, text_align=ft.TextAlign.CENTER)
    abrir_carpeta_button = ft.ElevatedButton("📂 Abrir carpeta de descargas", visible=False)

    # Agregar elementos a la página
    page.add(
        link_input,
        generar_button,
        qr_image,
        success_message,
        abrir_carpeta_button
    )

ft.app(target=main)