#!/usr/bin/env python3
"""Sprite Sheet Maker

Crea una spritesheet a partir de los frames (imágenes sueltas) de una carpeta.

Inputs (pedidos en terminal):
  - Ruta de la carpeta con los frames
  - Resolución de cada frame (ancho x alto)
  - Filas y columnas de la hoja final

Requiere Pillow:  pip install Pillow

Uso:
    python3 spritesheets_maker.py
"""

import os
import glob
import re
import sys
import math
import json
from pathlib import Path

from PIL import Image

# Extensiones de imagen soportadas.
SUPPORTED_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tiff")
# Patrón para ordenar nombres con bloque numérico (frame_001, frame2_10, etc.)
NUM_RE = re.compile(r"(\d+)")


def natural_sort_key(path: str) -> tuple:
    """Orden natural: frame_2 va antes que frame_10."""
    parts = NUM_RE.split(os.path.basename(path))
    return tuple(int(p) if p.isdigit() else p for p in parts)


def ask(prompt: str, default: str | None = None) -> str:
    """Pide un valor al usuario con un valor por defecto opcional."""
    suffix = f" [{default}]" if default is not None else ""
    print(f"  {prompt}{suffix}: ", end="", flush=True)
    value = input().strip()
    return value if value else (default if default is not None else "")


def ask_int(prompt: str, default: int) -> int:
    """Pide un entero válido; repite si la entrada es incorrecta."""
    while True:
        raw = ask(f"{prompt} (entero)", str(default))
        try:
            return int(raw)
        except ValueError:
            print(f"  '{raw}' no es un entero válido, probá de nuevo.")


def ask_path(prompt: str, default: str | None = None) -> str:
    """Pide una ruta de carpeta existente; repite si no existe."""
    while True:
        raw = ask(prompt, default)
        if not raw:
            print("  No se puede dejar vacío.")
            continue
        path = os.path.expanduser(raw)
        if os.path.isdir(path):
            return path
        print(f"  '{path}' no es una carpeta existente, probá de nuevo.")


def collect_frames(folder: str) -> list[str]:
    """Devuelve la lista ordenada de imágenes en la carpeta."""
    frames: list[str] = []
    for ext in SUPPORTED_EXTS:
        # glob.glob ya devuelve rutas completas, no hay que hacer join de nuevo
        frames.extend(glob.glob(os.path.join(folder, "*" + ext)))
        frames.extend(glob.glob(os.path.join(folder, "*" + ext.upper())))
    # Descartar duplicados si el FS es case-insensitive (Windows/macOS).
    seen: set[str] = set()
    unique: list[str] = []
    for f in frames:
        key = f.lower()
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return sorted(set(unique), key=natural_sort_key)


def main() -> int:
    print("=== Sprite Sheet Maker ===")
    print("Presioná Enter para usar el valor por defecto entre corchetes.\n")
    
    # Modo debug opcional
    debug = "--debug" in sys.argv or "-d" in sys.argv

    # Carpeta con frames
    default_folder = os.getcwd()
    folder = ask_path("Ruta con los frames", default_folder)
    frames = collect_frames(folder)

    if not frames:
        print(f"\nNo se encontraron imágenes en: {folder}")
        print("Soportadas:", ", ".join(SUPPORTED_EXTS))
        return 1

    print(f"\nSe encontraron {len(frames)} frame(s):")
    for f in frames[:10]:
        print("   -", os.path.basename(f))
    if len(frames) > 10:
        print(f"   ... y {len(frames) - 10} más")
    print()

    # Resolución de cada frame
    print("Resolución de cada frame (se redimensionan todos al mismo tamaño).")
    frame_w = ask_int("Ancho (px)", 64)
    frame_h = ask_int("Alto (px)", 64)
    if frame_w <= 0 or frame_h <= 0:
        print("La resolución debe ser positiva.")
        return 1

    # Columnas y filas
    print(
        "\nDistribución de la hoja. Ambas deben ser >= 1 y su producto >= número de frames."
    )
    min_cells = math.ceil(len(frames) / 1)
    default_cols = min(len(frames), 8)
    default_rows = math.ceil(len(frames) / default_cols)

    cols = ask_int("Columnas", default_cols)
    rows = ask_int("Filas", default_rows)

    if cols <= 0 or rows <= 0:
        print("Filas y columnas deben ser >= 1.")
        return 1
    if cols * rows < len(frames):
        print(
            f"\nLa hoja ({cols}x{rows} = {cols * rows}) no entra {len(frames)} frames."
        )
        # Ofrecer ajustar automáticamente.
        auto = (ask("¿Ajustar filas/cols para que entren? (s/n)", "s") + "").lower()
        if auto.startswith("s"):
            rows = math.ceil(len(frames) / cols)
            print(f"  Ajustado a {cols} columnas x {rows} filas.")
        else:
            print("Cancelado.")
            return 1

    total_w = cols * frame_w
    total_h = rows * frame_h
    print(f"\nDimensiones finales de la hoja: {total_w}x{total_h}px")

    # Salida
    default_output = os.path.join(folder, "spritesheet.png")
    while True:
        out_path = ask("Archivo de salida", default_output)
        if not out_path:
            print("  No se puede dejar vacío.")
            continue
        out_path = os.path.expanduser(out_path)
        out_dir = os.path.dirname(out_path) or "."
        if not os.path.isdir(out_dir):
            print(
                f"  La carpeta '{out_dir}' no existe. La creo...",
            )
            try:
                os.makedirs(out_dir, exist_ok=True)
            except OSError as e:
                print(f"  No se pudo crear la carpeta: {e}")
                continue
        break

    mode = (ask("\nColor (RGBA con transparencia / RGB sin transparencia)", "RGBA") + "").upper()
    if mode not in ("RGBA", "RGB"):
        print(f"Modo '{mode}' no reconocido, usando RGBA.")
        mode = "RGBA"
    
    # Preguntar si exportar JSON con rects
    export_json = (ask("\n¿Exportar archivo JSON con los rectángulos de cada frame? (s/n)", "s") + "").lower().startswith("s")
    json_path = None
    if export_json:
        default_json = out_path.rsplit(".", 1)[0] + ".json"
        json_path = ask("Archivo JSON de salida", default_json)
        json_path = os.path.expanduser(json_path)

    # Construir la hoja
    print(f"\nCreando spritesheet {total_w}x{total_h} en modo {mode}...")
    # Fondo transparente para RGBA, negro para RGB
    bg_color = (0, 0, 0, 0) if mode == "RGBA" else (0, 0, 0)
    sheet = Image.new(mode, (total_w, total_h), bg_color)
    
    # Metadata para JSON
    frame_rects = []

    for index, frame_path in enumerate(frames):
        if index >= cols * rows:
            print(f"  Aviso: hay más frames que celdas ({cols * rows}), ignorando el resto.")
            break
        col = index % cols
        row = index // cols
        x = col * frame_w
        y = row * frame_h
        try:
            img = Image.open(frame_path)
            if debug:
                print(f"    Debug: {os.path.basename(frame_path)} - Tamaño original: {img.size}, Modo: {img.mode}")
        except Exception as e:
            print(f"  No se pudo abrir {frame_path}: {e}")
            continue
        
        # Convertir y redimensionar
        img = img.convert(mode).resize((frame_w, frame_h), Image.Resampling.LANCZOS)
        
        if debug:
            # Verificar que la imagen no está vacía
            pixels = list(img.getdata())
            if mode == "RGBA":
                visible = sum(1 for p in pixels if p[3] > 0)
                print(f"    Debug: Píxeles visibles (alpha > 0): {visible}/{len(pixels)}")
            else:
                non_black = sum(1 for p in pixels if p != (0, 0, 0))
                print(f"    Debug: Píxeles no-negros: {non_black}/{len(pixels)}")
        
        # Pegar con canal alpha si está disponible
        if mode == "RGBA" and img.mode == "RGBA":
            sheet.paste(img, (x, y), img)
        else:
            sheet.paste(img, (x, y))
        
        # Guardar metadata del rect
        frame_name = os.path.splitext(os.path.basename(frame_path))[0]
        frame_rects.append({
            "name": frame_name,
            "x": x,
            "y": y,
            "width": frame_w,
            "height": frame_h,
            "index": index
        })
        
        print(f"  [{index + 1:>{len(str(len(frames)))}}/{len(frames)}] {os.path.basename(frame_path)} -> celda ({col},{row})")

    # Verificar que la hoja no esté vacía antes de guardar
    if debug:
        pixels = list(sheet.getdata())
        if mode == "RGBA":
            visible = sum(1 for p in pixels if p[3] > 0)
            print(f"\n  Debug FINAL: Píxeles visibles en spritesheet: {visible}/{len(pixels)} ({100*visible/len(pixels):.2f}%)")
        else:
            non_black = sum(1 for p in pixels if p != (0, 0, 0))
            print(f"\n  Debug FINAL: Píxeles no-negros en spritesheet: {non_black}/{len(pixels)} ({100*non_black/len(pixels):.2f}%)")
    
    sheet.save(out_path)
    print(f"\nSpritesheet guardada en: {out_path}")
    print(f"  Tamaño: {total_w}x{total_h} | {cols} cols x {rows} filas | {mode}")
    
    # Exportar JSON con rects si se solicitó
    if export_json and json_path:
        metadata = {
            "spritesheet": os.path.basename(out_path),
            "width": total_w,
            "height": total_h,
            "frame_width": frame_w,
            "frame_height": frame_h,
            "columns": cols,
            "rows": rows,
            "mode": mode,
            "total_frames": len(frame_rects),
            "frames": frame_rects
        }
        
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"\nMetadata JSON guardada en: {json_path}")
            print(f"  {len(frame_rects)} frames exportados")
        except Exception as e:
            print(f"\n  ADVERTENCIA: No se pudo guardar el JSON: {e}")
    
    # Verificación final sin debug
    if not debug:
        try:
            test = Image.open(out_path)
            print(f"\n  Verificado: archivo creado correctamente ({os.path.getsize(out_path)} bytes)")
        except Exception as e:
            print(f"  ADVERTENCIA: Error al verificar el archivo: {e}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelado.")
        sys.exit(130)
