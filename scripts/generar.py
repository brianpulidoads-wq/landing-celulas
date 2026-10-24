"""Genera las páginas de producto, el catálogo (productos.html) y la sección
de productos del index a partir de scripts/productos.json.

Uso (desde la raíz del repo):  python3 scripts/generar.py

Para agregar un producto: añade su bloque en productos.json, pon la foto en
img/productos/<slug>.jpg y vuelve a ejecutar el script.
"""
import json
import html
import re
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
WHATSAPP = "18132915034"
e = html.escape


def color_fondo(slug):
    """Color del borde de la foto, para que el recuadro se funda con ella."""
    try:
        from PIL import Image
        img = Image.open(RAIZ / "img/productos" / f"{slug}.jpg").convert("RGB")
        w, h = img.size
        pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
        r, g, b = [sum(img.getpixel(p)[i] for p in pts) // 4 for i in range(3)]
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return "#f0f4f1"


def wa(texto):
    return f"https://wa.me/{WHATSAPP}?text={quote(texto)}"


HEAD = """<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="description" content="{descripcion}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{ sans: ['"Plus Jakarta Sans"', 'sans-serif'] }},
                    colors: {{
                        clinical: {{ 50: '#f8faf8', 100: '#f0f4f1', 200: '#e1e9e3', 700: '#2d4d36', 800: '#1b3523', 900: '#0f2316' }},
                        neutral: {{ base: '#0f172a', muted: '#64748b', light: '#f8fafc', border: '#e2e8f0' }},
                        whatsapp: {{ DEFAULT: '#25D366', hover: '#20bd5a' }}
                    }}
                }}
            }}
        }}
    </script>
</head>
<body class="bg-[#ffffff] text-neutral-base font-sans antialiased selection:bg-clinical-100 selection:text-clinical-900 relative">

    <aside class="bg-clinical-900 text-white text-xs py-2.5 px-4 text-center tracking-wide font-medium">
        Suplementos naturales • Envíos seguros a todo Estados Unidos
    </aside>

    <header class="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-neutral-border">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 h-20 flex items-center justify-between gap-4">
            <a href="index.html" class="flex items-center gap-3 shrink-0">
                <img src="logo.png" alt="Natural World Services" class="h-10 sm:h-12 w-auto object-contain">
            </a>
            <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-neutral-muted">
                <a href="index.html" class="hover:text-clinical-900 transition-colors">Inicio</a>
                <a href="index.html#nosotros" class="hover:text-clinical-900 transition-colors">Nosotros</a>
                <a href="productos.html" class="{clase_productos}">Productos</a>
            </nav>
            <div class="flex items-center gap-3">
                <a href="productos.html" class="md:hidden text-sm font-semibold text-clinical-900">Productos</a>
                <a href="{wa_header}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 bg-clinical-900 text-white px-4 sm:px-5 py-2.5 rounded-full text-xs font-semibold tracking-wide hover:bg-clinical-800 transition-colors">
                    <span class="hidden sm:inline">Consultar con un asesor</span><span class="sm:hidden">Asesor</span>
                </a>
            </div>
        </div>
    </header>
"""

FOOT = """
    <footer class="border-t border-neutral-border py-12 text-xs text-neutral-muted bg-white">
        <div class="max-w-6xl mx-auto px-6 flex flex-col gap-6">
            <div class="flex flex-col sm:flex-row items-center justify-between gap-6 text-center sm:text-left">
                <div class="flex items-center gap-3 flex-col sm:flex-row">
                    <img src="logo.png" alt="Natural World Services" class="h-8 w-auto object-contain">
                    <span>Natural World Services • Suplementos y Salud Natural</span>
                </div>
                <p>© 2026 Natural World Services. Línea directa: +1 813 291 5034</p>
            </div>
            <p class="text-center sm:text-left leading-relaxed text-neutral-muted/90">
                Estas declaraciones no han sido evaluadas por la Administración de Alimentos y Medicamentos (FDA). Estos productos no están destinados a diagnosticar, tratar, curar ni prevenir ninguna enfermedad. Los resultados pueden variar según la persona. Consulta a tu médico antes de tomar suplementos si estás embarazada, en lactancia, tomas medicamentos o tienes una condición médica.
            </p>
        </div>
    </footer>

    <a href="{wa_flotante}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp" class="fixed bottom-6 right-6 bg-whatsapp text-white p-4 rounded-full shadow-2xl z-50 hover:bg-whatsapp-hover transition-transform hover:scale-110 flex items-center justify-center">
        <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 0C5.385 0 0 5.385 0 12.031c0 2.12.552 4.148 1.597 5.961L.12 24l6.196-1.46c1.748.948 3.702 1.455 5.715 1.455 6.646 0 12.031-5.385 12.031-12.031S18.677 0 12.031 0zm3.896 17.382c-.172.484-.984.953-1.461 1.023-.422.063-1.008.117-3.086-.742-2.5-1.031-4.102-3.602-4.227-3.766-.125-.164-1.008-1.344-1.008-2.563 0-1.219.633-1.820.859-2.055.227-.234.492-.297.656-.297.164 0 .328 0 .469.008.148.008.344-.055.539.414.195.469.664 1.625.727 1.75.063.125.102.273.016.445-.086.172-.133.273-.266.422-.125.156-.266.336-.383.453-.125.125-.258.266-.117.516.141.25.625 1.039 1.344 1.680.922.820 1.695 1.070 1.945 1.195.25.125.398.102.547-.063.148-.172.641-.75.813-1.008.172-.258.344-.219.57-.133.227.086 1.437.68 1.688.805.25.125.414.188.477.297.063.109.063.633-.109 1.117z"/></svg>
    </a>

</body>
</html>
"""

CHECK = '<svg class="w-5 h-5 shrink-0 text-clinical-700 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>'


def tarjeta(p, ruta_img="img/productos"):
    """Tarjeta reutilizada en el catálogo, el index y 'otros productos'."""
    return f"""
                <a href="{p['slug']}.html" data-categoria="{e(p['categoria'])}" class="producto-card group flex flex-col bg-white rounded-2xl border border-neutral-border overflow-hidden shadow-sm hover:shadow-lg hover:border-clinical-200 transition">
                    <div class="aspect-[4/3] flex items-center justify-center overflow-hidden" style="background:{color_fondo(p['slug'])}">
                        <img src="{ruta_img}/{p['slug']}.jpg" alt="{e(p['nombre'])}" loading="lazy" class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300">
                    </div>
                    <div class="p-6 flex flex-col flex-1">
                        <span class="text-clinical-700 text-[11px] font-bold uppercase tracking-wider mb-2">{e(p['categoria'])}</span>
                        <h3 class="text-lg font-bold text-neutral-base mb-2">{e(p['nombre'])}</h3>
                        <p class="text-sm text-neutral-muted leading-relaxed mb-5 flex-1">{e(p['frase'])}</p>
                        <span class="text-sm font-semibold text-clinical-900 inline-flex items-center gap-1">Ver producto <span class="group-hover:translate-x-1 transition-transform">→</span></span>
                    </div>
                </a>"""


def pagina_producto(p, todos):
    wa_pedido = wa(f"Hola, quiero pedir {p['nombre']}")
    wa_duda = wa(f"Hola, tengo una consulta sobre {p['nombre']}")

    chips = []
    if p.get("presentacion"):
        chips.append(f"Presentación: {e(p['presentacion'])}")
    if p.get("porcion"):
        chips.append(f"Porción: {e(p['porcion'])}")
    chips_html = "".join(
        f'<span class="px-3 py-1.5 rounded-full bg-neutral-light border border-neutral-border text-xs font-medium text-neutral-muted">{c}</span>'
        for c in chips
    )

    beneficios = "".join(
        f"""
                <li class="flex gap-3 p-5 rounded-2xl bg-white border border-neutral-border shadow-sm">
                    {CHECK}<span class="text-sm text-neutral-base leading-relaxed">{e(b)}</span>
                </li>"""
        for b in p["beneficios"]
    )

    filas = "".join(
        f"""
                <div class="p-6 grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-6">
                    <div class="sm:col-span-4">
                        <span class="block font-semibold text-neutral-base">{e(i['nombre'])}</span>
                        {f'<span class="text-sm font-semibold text-clinical-700">{e(i["cantidad"])}</span>' if i.get('cantidad') else ''}
                    </div>
                    <p class="sm:col-span-8 text-sm text-neutral-muted leading-relaxed">{e(i['detalle'])}</p>
                </div>"""
        for i in p["ingredientes"]
    )

    nota = (
        f'<p class="mt-6 text-sm text-neutral-muted leading-relaxed bg-clinical-50 border border-clinical-200 rounded-2xl p-5">{e(p["nota"])}</p>'
        if p.get("nota") else ""
    )
    precaucion = (
        f"""
            <div class="mt-6 flex gap-3 bg-amber-50 border border-amber-200 rounded-2xl p-5">
                <svg class="w-5 h-5 shrink-0 text-amber-600 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg>
                <p class="text-sm text-amber-900 leading-relaxed"><strong class="font-semibold">Precaución:</strong> {e(p['precaucion'])}</p>
            </div>"""
        if p.get("precaucion") else ""
    )

    otros = "".join(tarjeta(o) for o in todos if o["slug"] != p["slug"])

    cuerpo = f"""
    <main>
    <nav class="max-w-6xl mx-auto px-4 sm:px-6 pt-6 text-xs text-neutral-muted" aria-label="Ruta">
        <a href="index.html" class="hover:text-clinical-900">Inicio</a> <span class="mx-1">/</span>
        <a href="productos.html" class="hover:text-clinical-900">Productos</a> <span class="mx-1">/</span>
        <span class="text-neutral-base">{e(p['nombre'])}</span>
    </nav>

    <section class="max-w-6xl mx-auto px-4 sm:px-6 pt-8 pb-20">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-center">
            <div class="lg:col-span-6">
                <div class="rounded-3xl overflow-hidden border border-neutral-border shadow-xl shadow-neutral-200/60 aspect-[4/3] flex items-center justify-center" style="background:{color_fondo(p['slug'])}">
                    <img src="img/productos/{p['slug']}.jpg" alt="{e(p['nombre'])}" class="w-full h-full object-contain">
                </div>
            </div>
            <div class="lg:col-span-6">
                <div class="inline-flex items-center px-3 py-1 rounded-full bg-clinical-50 border border-clinical-200 text-clinical-700 text-xs font-semibold uppercase tracking-wider mb-5">{e(p['categoria'])}</div>
                <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight text-neutral-base leading-tight mb-4">{e(p['nombre'])}</h1>
                <p class="text-xl text-clinical-800 font-semibold mb-5">{e(p['frase'])}</p>
                <p class="text-base text-neutral-muted leading-relaxed mb-6">{e(p['resumen'])}</p>
                <div class="flex flex-wrap gap-2 mb-8">{chips_html}</div>
                <div class="flex flex-col sm:flex-row gap-3">
                    <a href="{wa_pedido}" target="_blank" rel="noopener" class="text-center bg-clinical-900 text-white px-8 py-4 rounded-xl font-semibold text-sm hover:bg-clinical-800 transition shadow-sm">Pedir por WhatsApp</a>
                    <a href="#ingredientes" class="text-center bg-white text-neutral-base border border-neutral-border px-8 py-4 rounded-xl font-semibold text-sm hover:bg-neutral-light transition">Ver ingredientes</a>
                </div>
            </div>
        </div>
    </section>

    <section class="bg-clinical-50/40 border-y border-neutral-border py-20">
        <div class="max-w-6xl mx-auto px-4 sm:px-6">
            <span class="text-clinical-700 text-xs font-bold uppercase tracking-wider">Beneficios</span>
            <h2 class="text-3xl font-bold tracking-tight text-neutral-base mt-2 mb-10">¿En qué te puede ayudar?</h2>
            <ul class="grid grid-cols-1 md:grid-cols-2 gap-4">{beneficios}
            </ul>
        </div>
    </section>

    <section id="ingredientes" class="max-w-4xl mx-auto px-4 sm:px-6 py-20 scroll-mt-24">
        <div class="text-center mb-10">
            <span class="text-clinical-700 text-xs font-bold uppercase tracking-wider">Fórmula</span>
            <h2 class="text-3xl font-bold tracking-tight text-neutral-base mt-2">Ingredientes y su función</h2>
            {f'<p class="text-sm text-neutral-muted mt-3">Cantidades por porción de {e(p["porcion"])}, según la etiqueta.</p>' if p.get('porcion') and any(i.get('cantidad') for i in p['ingredientes']) else ''}
        </div>
        <div class="border border-neutral-border rounded-2xl bg-white shadow-sm divide-y divide-neutral-border">{filas}
        </div>
        {nota}{precaucion}
    </section>

    <section class="max-w-5xl mx-auto px-4 sm:px-6 pb-20">
        <div class="bg-clinical-900 rounded-3xl p-8 sm:p-12 text-center text-white shadow-xl shadow-clinical-900/10">
            <h2 class="text-2xl sm:text-3xl font-bold mb-4">¿Es {e(p['nombre'])} para ti?</h2>
            <p class="text-neutral-200 text-sm sm:text-base max-w-xl mx-auto mb-8 leading-relaxed">Cuéntale tu caso a un asesor y te orienta sobre cómo tomarlo y por cuánto tiempo.</p>
            <a href="{wa_duda}" target="_blank" rel="noopener" class="inline-block bg-white text-clinical-900 px-8 py-4 rounded-xl font-semibold text-sm hover:bg-neutral-light transition shadow-md">Hablar con un asesor por WhatsApp</a>
            <p class="mt-4 text-sm text-neutral-300 font-medium">Envío gratuito • Disponible en todo EE. UU. • Pago seguro</p>
        </div>
    </section>

    <section class="border-t border-neutral-border py-20 bg-neutral-light/40">
        <div class="max-w-6xl mx-auto px-4 sm:px-6">
            <h2 class="text-2xl font-bold tracking-tight text-neutral-base mb-8">Otros productos</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">{otros}
            </div>
        </div>
    </section>
    </main>
"""
    return (
        HEAD.format(
            titulo=f"{p['nombre']} | Natural World Services",
            descripcion=e(p["resumen"]),
            clase_productos="text-clinical-900 font-semibold",
            wa_header=wa_duda,
        )
        + cuerpo
        + FOOT.format(wa_flotante=wa_duda)
    )


def pagina_catalogo(todos):
    categorias = []
    for p in todos:
        if p["categoria"] not in categorias:
            categorias.append(p["categoria"])
    filtros = '<button type="button" data-filtro="todos" class="filtro px-4 py-2 rounded-full text-sm font-semibold border transition bg-clinical-900 text-white border-clinical-900">Todos</button>' + "".join(
        f'<button type="button" data-filtro="{e(c)}" class="filtro px-4 py-2 rounded-full text-sm font-semibold border transition bg-white text-neutral-muted border-neutral-border hover:border-clinical-700">{e(c)}</button>'
        for c in categorias
    )
    tarjetas = "".join(tarjeta(p) for p in todos)
    wa_gen = wa("Hola, quisiera asesoría sobre sus productos")
    cuerpo = f"""
    <main>
    <section class="bg-clinical-50/40 border-b border-neutral-border py-16">
        <div class="max-w-6xl mx-auto px-4 sm:px-6">
            <span class="text-clinical-700 text-xs font-bold uppercase tracking-wider">Catálogo</span>
            <h1 class="text-4xl font-extrabold tracking-tight text-neutral-base mt-2 mb-4">Nuestros productos</h1>
            <p class="text-neutral-muted text-lg max-w-2xl leading-relaxed">Suplementos naturales para cada necesidad. Elige el tuyo o escríbenos y un asesor te ayuda a encontrar el indicado.</p>
        </div>
    </section>

    <section class="max-w-6xl mx-auto px-4 sm:px-6 py-12">
        <div class="flex flex-wrap gap-2 mb-10" role="group" aria-label="Filtrar por categoría">{filtros}</div>
        <div id="grid-productos" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">{tarjetas}
        </div>
    </section>
    </main>

    <script>
        document.querySelectorAll('.filtro').forEach(function (btn) {{
            btn.addEventListener('click', function () {{
                var f = btn.dataset.filtro;
                document.querySelectorAll('.filtro').forEach(function (b) {{
                    var activo = b === btn;
                    b.classList.toggle('bg-clinical-900', activo);
                    b.classList.toggle('text-white', activo);
                    b.classList.toggle('border-clinical-900', activo);
                    b.classList.toggle('bg-white', !activo);
                    b.classList.toggle('text-neutral-muted', !activo);
                    b.classList.toggle('border-neutral-border', !activo);
                }});
                document.querySelectorAll('.producto-card').forEach(function (c) {{
                    c.style.display = (f === 'todos' || c.dataset.categoria === f) ? '' : 'none';
                }});
            }});
        }});
    </script>
"""
    return (
        HEAD.format(
            titulo="Productos | Natural World Services",
            descripcion="Catálogo de suplementos naturales de Natural World Services.",
            clase_productos="text-clinical-900 font-semibold",
            wa_header=wa_gen,
        )
        + cuerpo
        + FOOT.format(wa_flotante=wa_gen)
    )


def seccion_index(todos):
    tarjetas = "".join(tarjeta(p) for p in todos)
    return f"""<!-- PRODUCTOS:INICIO (generado por scripts/generar.py, no editar a mano) -->
    <section id="productos" class="max-w-6xl mx-auto px-6 py-24 scroll-mt-24">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-6 mb-12">
            <div class="max-w-2xl">
                <span class="text-clinical-700 text-xs font-bold uppercase tracking-wider">Nuestra línea</span>
                <h2 class="text-3xl font-bold tracking-tight text-neutral-base mt-2 mb-3">Más productos para tu bienestar</h2>
                <p class="text-neutral-muted text-base leading-relaxed">Además de AFA, contamos con fórmulas para circulación, articulaciones, energía y salud masculina.</p>
            </div>
            <a href="productos.html" class="shrink-0 text-sm font-semibold text-clinical-900 border border-neutral-border rounded-full px-5 py-2.5 hover:bg-neutral-light transition">Ver catálogo completo →</a>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">{tarjetas}
        </div>
    </section>
    <!-- PRODUCTOS:FIN -->"""


def main():
    todos = json.loads((RAIZ / "scripts/productos.json").read_text(encoding="utf-8"))
    for p in todos:
        (RAIZ / f"{p['slug']}.html").write_text(pagina_producto(p, todos), encoding="utf-8")
    (RAIZ / "productos.html").write_text(pagina_catalogo(todos), encoding="utf-8")

    index = RAIZ / "index.html"
    txt = index.read_text(encoding="utf-8")
    nueva = seccion_index(todos)
    if "<!-- PRODUCTOS:INICIO" in txt:
        txt = re.sub(r"<!-- PRODUCTOS:INICIO.*?<!-- PRODUCTOS:FIN -->", lambda m: nueva, txt, flags=re.S)
    else:
        txt = txt.replace("    <!-- Logística y Garantías -->", "    " + nueva + "\n\n    <!-- Logística y Garantías -->", 1)
    index.write_text(txt, encoding="utf-8")
    print(f"OK: {len(todos)} productos generados")


if __name__ == "__main__":
    main()
