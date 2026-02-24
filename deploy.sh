mpremote connect auto fs cp main.py :
mpremote connect auto fs mkdir lib
mpremote connect auto fs cp lib/arch.py :lib/arch.py
mpremote connect auto fs cp lib/graphics.py :lib/graphics.py
mpremote connect auto fs cp lib/text_renderer.py :lib/text_renderer.py
mpremote connect auto fs cp lib/constants.py :lib/constants.py
mpremote connect auto fs cp lib/st7789py.py :lib/st7789py.py
mpremote connect auto fs cp lib/__init__.py :lib/__init__.py
mpremote connect auto reset

