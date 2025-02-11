function verProducto(img, nombre, precio, desc) {
    window.location.href = `producto.html?img=${encodeURIComponent(img)}&nombre=${encodeURIComponent(nombre)}&precio=${encodeURIComponent(precio)}&desc=${encodeURIComponent(desc)}`;
}


function toggleMenu() {
    const menu = document.getElementById("nav-menu");
    menu.classList.toggle("active");
}
