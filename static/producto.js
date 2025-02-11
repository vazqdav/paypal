document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const img = urlParams.get("img");
    const nombre = urlParams.get("nombre");
    const precio = urlParams.get("precio");
    const desc = urlParams.get("desc");

    console.log(img, nombre, precio, desc);  // Verificar los parámetros

    if (img && nombre && precio && desc) {
        // Asegúrate de que la ruta es correcta
        document.getElementById("producto-img").src = "/static/img/" + decodeURIComponent(img);  // Usar la ruta correcta
        document.getElementById("producto-nombre").textContent = decodeURIComponent(nombre);
        document.getElementById("producto-precio").textContent = "$" + decodeURIComponent(precio);  // Agregar signo de peso
        document.getElementById("producto-desc").textContent = decodeURIComponent(desc);
    } else {
        document.getElementById("detalle-producto").innerHTML = "<h2>Producto no encontrado</h2>";
    }
});
