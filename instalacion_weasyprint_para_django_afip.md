# 📝 Instalación de WeasyPrint en Windows 10/11 (Python 64 bits)

Este documento resume todos los pasos necesarios para instalar **WeasyPrint** correctamente en Windows usando **Python 64 bits**, **MSYS2**, **GTK3**, **Cairo** y un entorno virtual limpio.

---

## ✅ 1. Instalar Python 64 bits

1. Descargar Python 64 bits desde [https://python.org](https://python.org)

2. Durante la instalación:

   * Activar **"Add Python to PATH"**

   * Instalar normalmente.

Verificar versión e instalación:

```bash
python --version
where python
```

Debe aparecer un Python de **64 bits**.

---

## ✅ 2. Instalar MSYS2

1. Descargar MSYS2 (64 bits) desde: [https://www.msys2.org/](https://www.msys2.org/)

2. Instalar normalmente.

3. Abrir **MSYS2 MSYS** y ejecutar:

```bash
pacman -Syu
```

Cerrar y volver a abrir, luego:

```bash
pacman -Su
```

Agregar al PATH de Windows:

```
C:\msys64\usr\bin
```

---

## ✅ 3. Instalar GTK3 + Cairo + Pango (64 bits)

Dentro de **MSYS2 MINGW64**, ejecutar:

```bash
pacman -S mingw-w64-x86_64-gtk3
pacman -S mingw-w64-x86_64-pango
pacman -S mingw-w64-x86_64-cairo
pacman -S mingw-w64-x86_64-gdk-pixbuf2
```

Confirmar instalación de Cairo:

```bash
where libcairo-2.dll
```

Debe apuntar a:

```
C:\msys64\mingw64\bin\libcairo-2.dll
```

---

## ✅ 4. Crear un entorno virtual nuevo

Si existía un venv anterior (32 bits), eliminarlo.

Crear nuevo entorno virtual con Python 64 bits:

```bash
python -m venv venv
```

Activar:

```bash
venv\Scripts\activate
```

---

## ✅ 5. Instalar dependencias del proyecto

Si ya tenés un `requirements.txt`:

```bash
pip install -r requirements.txt
```

Si instalás manualmente:

```bash
pip install weasyprint
```

---

## ✅ 6. Probar WeasyPrint

Crear un archivo `test.html` y ejecutar:

```python
from weasyprint import HTML
HTML("test.html").write_pdf("test.pdf")
```

Debe generarse un PDF sin errores relacionados a Cairo/Pango/GDK/GTK.

---

## 🎉 ¡Listo! WeasyPrint funciona en Windows con Python 64 bits

Si querés, también puedo armarte una **versión .ps1 (PowerShell)** para automatizar toda la instalación en cualquier equipo.

