from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file
import paypalrestsdk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# Configuración de PayPal (deberás ingresar tus credenciales de PayPal)
paypalrestsdk.configure({
    "mode": "sandbox",  # Cambia "live para pagos reales" y "sandbox para pruebas"
    "client_id": "tu client id aquí",  # Reemplaza con tu Client ID
    "client_secret": "tu client secret aquí"  # Reemplaza con tu Client Secret
})

productos = [
    {'id': 1, 'nombre': 'Producto 1', 'descripcion': 'Descripción del Producto 1', 'precio': 20.00, 'imagen': 'playera.webp'},
    {'id': 2, 'nombre': 'Producto 2', 'descripcion': 'Descripción del Producto 2', 'precio': 40.00, 'imagen': 'mochila.webp'},
    {'id': 3, 'nombre': 'Producto 3', 'descripcion': 'Descripción del Producto 3', 'precio': 40.00, 'imagen': 'teniz.webp'}
]

# Función para obtener un producto por ID
def obtener_producto_por_id(producto_id):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None

# Ruta para mostrar todos los productos
@app.route('/')
def index():
    return render_template('index.html', productos=productos)

# Ruta para ver los detalles de un producto específico
@app.route('/producto/<int:producto_id>')
def producto_detalle(producto_id):
    producto = next((prod for prod in productos if prod['id'] == producto_id), None)
    if producto:
        return render_template('producto.html', producto=producto)
    else:
        return "Producto no encontrado", 404

# Ruta para crear el pago
@app.route('/crear_pago', methods=['POST'])
def crear_pago():
    producto_id = request.form.get('producto_id')
    producto = next((p for p in productos if p['id'] == int(producto_id)), None)

    if producto is None:
        return jsonify({'error': 'Producto no encontrado'}), 404

    # Crear la orden de pago
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": str(producto['precio']), "currency": "MXN"},
            "description": producto['nombre']
        }],
       "redirect_urls": {
    "return_url": "http://127.0.0.1:5000/pago_exitoso",
    "cancel_url": "http://127.0.0.1:5000/pago_cancelado"
}
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                print("Redirigiendo a:", approval_url)  # <-- Agrega esto para depurar
                return redirect(approval_url)
    else:
        return jsonify({'error': 'Error al crear el pago de PayPal'}), 500

# Ruta para manejar la respuesta de PayPal (cuando el pago es aprobado)
from flask import render_template

@app.route('/pago_exitoso')
def pago_exitoso():
    payment_id = request.args.get("paymentId")
    payer_id = request.args.get("PayerID")
    payer_name = request.args.get("payerName")  # Ahora obtenemos el nombre del pagador desde la URL

    if not payment_id or not payer_id:
        return jsonify({
            "error": "Faltan parámetros de pago",
            "payerId": payer_id,
            "paymentId": payment_id,
            "payerName": payer_name,
            "debug_info": request.args
        }), 400

    return render_template("pago_exitoso.html", paymentId=payment_id, payerId=payer_id, payerName=payer_name or 'Desconocido')



# Ruta para manejar cuando el pago es cancelado
@app.route('/pago_cancelado')
def pago_cancelado():
    return render_template('pago_cancelado.html')


@app.route('/descargar_pdf')
def descargar_pdf():
    payment_id = request.args.get("paymentId")
    payer_id = request.args.get("PayerID")
    payer_name = request.args.get("payerName", "Cliente Desconocido")

    if not payment_id or not payer_id:
        return "Faltan datos para generar el PDF", 400

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Recibo de Pago")

    # Estilos del PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Recibo de Pago")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 700, f"Nombre del Cliente: {payer_name}")
    pdf.drawString(100, 680, f"ID de Pago: {payment_id}")
    pdf.drawString(100, 660, f"ID del Pagador: {payer_id}")
    pdf.drawString(100, 640, "Gracias por tu compra!")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Recibo_Pago.pdf", mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
