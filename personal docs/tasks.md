# Tareas de desarrollo

Lista de continuidad del proyecto. Las tareas marcadas reflejan el estado al cierre de la sesión del 2026-09-05.

## Completado: base del cliente

- [X] Crear ventana Pygame-ce.
- [X] Crear bucle de frames y cierre seguro.
- [X] Separar `World`, `Simulation` y `SimulationClock`.
- [X] Añadir HUD con tick, FPS, pausa y velocidad.
- [X] Añadir velocidades de `x1` a `x10`.
- [X] Crear contrato base de escenas.
- [X] Crear `MainMenuScene`.
- [X] Crear `WorldScene`.
- [X] Conectar `Create world` con la transición a `WorldScene`.
- [X] Dibujar cuadrícula.
- [X] Convertir el mouse a coordenadas de celda.
- [X] Mostrar `hovered_cell` y `selected_cell` en debug.
- [X] Mantener el inventario centrado y adaptable al redimensionamiento.

## Completado: UI de construcción e inventario

- [X] Crear `ConstructionMenu` como clase separada.
- [X] Crear panel de construcción y opciones dinámicas.
- [X] Mantener `selected_construction` hasta cancelar.
- [X] Crear `InventoryPanel` modal con tecla `E`.
- [X] Ocultar el menú de construcción cuando el inventario está abierto.
- [X] Crear 27 slots visuales en distribución 9×3.
- [X] Detectar qué slot fue pulsado.
- [X] Mostrar el contenido de los slots desde `InventoryInstance`.

## Completado: items e inventario

- [X] Crear `ItemStackInstance`.
- [X] Añadir datos opcionales a los stacks.
- [X] Comparar compatibilidad por `item_id` y datos.
- [X] Copiar stacks sin compartir datos mutables.
- [X] Validar cantidades positivas.
- [X] Crear `InventoryInstance` basado en slots.
- [X] Resolver `ItemDefinition` mediante `Registry`.
- [X] Implementar `get_slot` y `set_slot`.
- [X] Implementar `get_quantity` y `contains`.
- [X] Implementar `can_add` y `add_stack`.
- [X] Implementar `consume` y `copy`.
- [X] Respetar `max_stack_size` y dividir lotes entre slots.

## Completado: base modular de definiciones y órdenes

- [X] Crear `ConstructionType`.
- [X] Crear `Registry[T]` genérico.
- [X] Crear `GameDefinitions` como catálogo central.
- [X] Hacer que `World` conserve un catálogo de definiciones.
- [X] Crear `PlaceConstructionOrder` genérica.
- [X] Crear `OrderResult`.
- [X] Crear `OrderSystem` con cola FIFO.
- [X] Procesar órdenes al inicio de un tick.
- [X] Crear `ConstructionHandler` registrable.
- [X] Separar reglas específicas de fábrica en `FactoryConstructionHandler`.
- [X] Validar definición de construcción.
- [X] Validar ocupación de la celda.
- [X] Validar coste y recursos del inventario.
- [X] Consumir recursos solo después de validar.
- [X] Crear instancia de fábrica y añadirla a `World`.
- [X] Dibujar placeholder de construcciones colocadas.
- [X] Eliminar el mundo de prueba hardcodeado de `App`.

## Próximo bloque: contenido real

- [ ] Crear `JsonLoader`.
- [ ] Crear `DefinitionParser`.
- [ ] Crear `DefinitionValidator`.
- [ ] Cargar definiciones desde una plantilla externa.
- [ ] Registrar items y fábricas en `GameDefinitions` desde datos externos.
- [ ] Hacer que `ConstructionMenu` muestre las opciones cargadas.
- [ ] Mostrar `OrderResult` en la UI en lugar de usar `print()`.

## Próximo bloque: tipos de construcción

- [ ] Crear `ResourceNodeDefinition` y `ResourceNode`.
- [ ] Crear `SuProducerDefinition` y `SuProducer`.
- [ ] Crear handlers para productores de SU.
- [ ] Mantener los nodos como entidades generadas por el mundo, no como items colocables.
- [ ] Añadir minas como construcciones colocables sobre nodos.
- [ ] Añadir almacenes y contenedores como construcciones colocables.

## Próximo bloque: módulos y producción

- [ ] Crear `AddModuleOrder` para módulos internos de una fábrica.
- [ ] Validar slots disponibles según el nivel de la fábrica.
- [ ] Crear `UpgradeFactoryOrder`.
- [ ] Crear `UpgradeModuleOrder`.
- [ ] Crear máquinas y recetas desde definiciones cargadas.
- [ ] Crear `MachineTask`.
- [ ] Ejecutar progreso por ticks.
- [ ] Guardar outputs en buffers.
- [ ] Entregar outputs a contenedores.

## Más adelante

- [ ] Crear `GameLog` y eventos de simulación.
- [ ] Crear belts lineales A → B.
- [ ] Añadir transporte de items en belts.
- [ ] Trenes y estaciones.
- [ ] Redes de SU completas y prioridades.
- [ ] Guardados y carga del estado del mundo.
- [ ] Generación procedural.
- [ ] Prospección de nodos ocultos.
- [ ] Portales y transporte cuántico.
- [ ] Settings completos.
- [ ] Editor de definiciones dentro del juego.

## Contexto breve para mañana

El sistema ya no debe volver a añadir fábricas o items de prueba directamente en `App`. `App` crea un `GameDefinitions` vacío y un `World`; el contenido debe llegar mediante registros cargados desde una fuente externa.

La siguiente tarea recomendada es el flujo:

```text
JSON de plantilla
→ JsonLoader
→ DefinitionParser
→ DefinitionValidator
→ GameDefinitions
→ ConstructionMenu dinámico
→ PlaceConstructionOrder
```

La arquitectura actual distingue:

```text
ResourceNode:
    generado por el mundo

Factory y SuProducer:
    construcciones colocables

Module y Machine:
    instancias internas de una fábrica
```

No mezclar estas categorías en una única orden.

## Reglas de trabajo

- Trabajar por un slice pequeño y visible.
- No mezclar lógica de Pygame con modelos del juego.
- La UI crea órdenes; no modifica `World` directamente.
- Las definiciones viven en `GameDefinitions`, no en `App` ni dispersas en `World`.
- Añadir tipos nuevos mediante registros y handlers, no mediante condicionales repartidos.
- No crear archivos nuevos sin una responsabilidad concreta.
- Probar cada slice antes de añadir el siguiente.
- Explicar el código generado antes de continuar con la siguiente capa.
