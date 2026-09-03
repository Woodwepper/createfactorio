# Tareas de desarrollo

Lista de continuidad para retomar el proyecto después de una pausa.

## Estado actual

La aplicación ya tiene una ventana Pygame-ce, escenas, menú principal, transición a un mundo nuevo, HUD, ticks, pausa y velocidades de `x1` a `x10`.

## Próximo objetivo: cerrar el flujo visual básico

- [X] Ejecutar manualmente `python main.py`.
- [X] Comprobar que aparece `MainMenuScene`.
- [X] Pulsar `Create world`.
- [X] Confirmar que aparece `WorldScene`.
- [X] Confirmar que el contador de ticks aumenta.
- [X] Confirmar que `Pause` cambia a `Resume`.
- [X] Confirmar que `Speed +1` y `Speed -1` respetan `x1` y `x10`.
- [X] Confirmar que `Exit` y `Escape` cierran correctamente.

## Slice visual 1: mapa placeholder

- [ ] Crear una cuadrícula visible en `WorldScene`.
- [ ] Separar el renderizado de la cuadrícula en `client/rendering/grid_renderer.py`.
- [ ] Mostrar coordenadas o una celda seleccionada.
- [ ] Añadir una primera representación placeholder de un nodo de recursos.

## Slice de órdenes

- [ ] Definir la estructura base de `Order`.
- [ ] Definir `OrderResult`.
- [ ] Crear la cola y el despacho de `OrderSystem`.
- [ ] Crear `GameLog` para órdenes, resultados y eventos.
- [ ] Procesar órdenes al inicio de un tick.
- [ ] Implementar `PlaceBuildingOrder` como primera orden real.
- [ ] Mostrar en el cliente el resultado exitoso o fallido de una orden.

## Slice de items y almacenamiento

- [ ] Crear `ItemStack` con `item_id`, `amount` y datos opcionales.
- [ ] Definir cuándo dos stacks pueden combinarse.
- [ ] Crear `Inventory` por slots.
- [ ] Implementar `add_item`, `consume`, `contains`, `get_quantity`, `can_add` y `copy`.
- [ ] Crear `Container` como construcción que posee un inventario.
- [ ] Mostrar un inventario sencillo mediante `pygame_gui`.

## Slice de construcciones

- [ ] Crear una definición y modelo mínimo de fábrica.
- [ ] Crear una orden para colocar una fábrica.
- [ ] Validar posición y ocupación de la cuadrícula.
- [ ] Consumir el item de construcción.
- [ ] Dibujar un placeholder de fábrica en el mapa.
- [ ] Crear el flujo inicial de mina sobre un nodo.

## Slice de producción

- [ ] Crear `MachineDefinition` y `RecipeDefinition` mínimas en memoria.
- [ ] Crear `MachineTask`.
- [ ] Crear un módulo dentro de una fábrica.
- [ ] Insertar una máquina en el módulo.
- [ ] Asignar una receta.
- [ ] Consumir inputs al asignar una tarea.
- [ ] Ejecutar progreso por ticks.
- [ ] Guardar outputs en `output_buffer`.
- [ ] Entregar outputs a un contenedor.

## Slice de SU

- [ ] Crear un productor de SU.
- [ ] Crear un hub de SU.
- [ ] Crear conexiones abstractas entre productores y consumidores.
- [ ] Crear prioridades base y prioridad modificable.
- [ ] Distribuir SU por prioridad.
- [ ] Pausar construcciones completas que no reciban toda su demanda.
- [ ] Mostrar visualmente el estado de alimentación.

## Slice de belts

- [ ] Crear un belt lineal A → B.
- [ ] Mover items visualmente dentro del belt.
- [ ] Mantener items dentro del belt si el destino está lleno.
- [ ] No permitir bifurcaciones en la primera versión.
- [ ] Conectar posteriormente belts con contenedores y construcciones.

## Más adelante

- [ ] Carga y validación de definiciones JSON.
- [ ] `GameDefinitions` y registros.
- [ ] Guardados y carga del estado del mundo.
- [ ] Trenes y estaciones.
- [ ] Portales y transporte cuántico.
- [ ] Generación procedural del mapa.
- [ ] Prospección de nodos ocultos.
- [ ] Settings completos.
- [ ] Editor de definiciones dentro del juego.

## Reglas de trabajo

- Trabajar por un slice pequeño y visible.
- No mezclar lógica de Pygame con modelos del juego.
- La UI crea órdenes; no modifica el `World` directamente.
- No crear archivos nuevos sin una responsabilidad concreta.
- Probar cada slice antes de añadir el siguiente.
