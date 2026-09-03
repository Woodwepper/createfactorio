# Estructura estable del proyecto

Esta estructura separa simulación, contenido, cliente y herramientas sin crear capas innecesarias. Las carpetas existen para durar durante todo el proyecto, pero los archivos concretos se crearán solo cuando una mecánica los necesite.

```text
project/
├── context.md                       # Memoria de continuidad y decisiones
├── design_questions_answers.md      # Preguntas y respuestas de diseño
├── gameplay_ideas.md                # Lluvia de ideas y mecánicas futuras
├── folder_structure.md              # Este documento
├── main.py                          # Punto de entrada de la aplicación
├── README.md                        # Se creará al definir instalación y ejecución
├── pyproject.toml                   # Se creará al fijar dependencias
│
├── game/
│   ├── __init__.py
│   └── logic/
│       ├── __init__.py
│       │
│       ├── core/                    # Ciclo global y estado de la partida
│       │   ├── __init__.py
│       │   ├── world.py             # Contenedor de instancias vivas
│       │   ├── simulation.py        # Orquestador externo de ticks
│       │   └── game_log.py          # Eventos y resultados para cliente/debug
│       │
│       ├── orders/                  # Intenciones del jugador y resultados
│       │   ├── __init__.py
│       │   ├── order.py             # Estructura base de una orden
│       │   ├── order_result.py
│       │   ├── order_system.py
│       │   ├── construction_orders.py
│       │   ├── production_orders.py
│       │   └── logistics_orders.py
│       │
│       ├── definitions/             # Datos estáticos e inmutables
│       │   ├── __init__.py
│       │   ├── item_definition.py
│       │   ├── machine_definition.py
│       │   ├── recipe_definition.py
│       │   ├── module_definition.py
│       │   ├── factory_definition.py
│       │   ├── resource_node_definition.py
│       │   ├── su_producer_definition.py
│       │   └── resource_requirement.py
│       │
│       ├── enums/                   # Estados y categorías
│       │   ├── __init__.py
│       │   ├── machine_state.py
│       │   ├── module_state.py
│       │   ├── factory_state.py
│       │   ├── su_producer_state.py
│       │   ├── item_category.py
│       │   └── resource_type.py
│       │
│       ├── models/                  # Instancias mutables del World
│       │   ├── __init__.py
│       │   ├── item_stack.py
│       │   ├── inventory.py
│       │   ├── container.py
│       │   ├── machine.py
│       │   ├── machine_task.py
│       │   ├── module.py
│       │   ├── factory.py
│       │   ├── mine.py
│       │   ├── resource_node.py
│       │   ├── su_hub.py
│       │   ├── su_network.py
│       │   ├── su_producer.py
│       │   └── belt.py
│       │
│       ├── systems/                 # Reglas que actualizan modelos
│       │   ├── __init__.py
│       │   ├── construction_system.py
│       │   ├── production_system.py
│       │   ├── su_system.py
│       │   ├── extraction_system.py
│       │   └── logistics_system.py
│       │
│       └── content/                 # Contenido externo y persistencia futura
│           ├── __init__.py
│           ├── registry.py
│           ├── game_definitions.py
│           ├── json_loader.py
│           ├── definition_parser.py
│           ├── definition_validator.py
│           └── save_manager.py
│
├── client/
│   ├── __init__.py
│   ├── app.py                        # Bucle Pygame-ce y ciclo de frames
│   │
│   ├── scenes/                       # Menú, mundo, pausa, etc.
│   │   ├── __init__.py
│   │   ├── scene.py
│   │   └── world_scene.py
│   │
│   ├── rendering/                    # Dibuja, no modifica la lógica
│   │   ├── __init__.py
│   │   ├── camera.py
│   │   ├── grid_renderer.py
│   │   ├── world_renderer.py
│   │   └── sprite_animation.py
│   │
│   ├── interaction/                  # Input y modos de acción
│   │   ├── __init__.py
│   │   ├── input_handler.py
│   │   ├── selection_mode.py
│   │   └── construction_mode.py
│   │
│   ├── ui/                           # UI custom y pygame_gui
│   │   ├── __init__.py
│   │   ├── hud.py
│   │   ├── inventory_panel.py
│   │   ├── construction_panel.py
│   │   ├── factory_panel.py
│   │   └── game_log_panel.py
│   │
│   └── assets/
│       ├── spritesheets/
│       ├── textures/
│       └── sounds/
│
├── data/
│   ├── templates/
│   │   └── default/                  # Plantilla editable del juego
│   │       ├── items/
│   │       ├── machines/
│   │       ├── recipes/
│   │       ├── modules/
│   │       ├── factories/
│   │       ├── resource_nodes/
│   │       └── su_producers/
│   └── saves/                        # Estados de partidas
│
├── tools/
│   └── spritesheets_maker.py         # Mover aquí cuando decidamos ordenar herramientas
│
├── blockbench models/                # Archivos fuente de modelos visuales
│
└── tests/
    ├── unit/                         # Modelos y sistemas aislados
    └── integration/                  # Simulation + World + órdenes
```

## Responsabilidades y reglas de importación

### `game/logic`

No importa `pygame`, `pygame_gui` ni recursos gráficos.

```text
logic
→ puede ejecutarse desde pruebas, consola o cliente
→ no dibuja
→ no lee clicks directamente
```

### `client`

Importa la lógica y la representa.

```text
client
→ lee estado del World
→ crea órdenes según input
→ las envía a Simulation
→ dibuja el resultado
```

La UI no modifica directamente objetos del `World`.

### `core`

Contiene el ciclo general:

```text
World
→ Simulation
→ OrderSystem
→ Systems
→ GameLog
```

### `orders`

Contiene las intenciones del jugador. Cada orden usa identificadores y datos simples, no referencias directas a modelos vivos.

### `definitions` y `models`

```text
Definition:
    describe qué puede existir.

Model:
    representa una instancia viva de una partida.
```

### `systems`

Un sistema contiene reglas transversales y se especializa por dominio. Por ejemplo, `SuSystem` distribuye capacidad; `ProductionSystem` procesa recetas.

### `content`

Se utilizará cuando se implemente carga de JSON, validación de definiciones, registros y guardados. No bloquea el MVP en memoria.

## Regla para añadir archivos

No crear un archivo solo porque aparece en el árbol. Se crea cuando existe una responsabilidad real y una primera prueba o caso de uso.

Ejemplo:

```text
No crear Train, RailNetwork o Portal ahora.

Crear belt.py cuando se implemente el primer belt A → B.
Crear su_network.py cuando se implemente el hub y la distribución de SU.
Crear world_scene.py cuando ya exista una ventana y una cuadrícula que mostrar.
```

## Flujo de dependencias

```text
client
    ↓ órdenes / consultas
logic.core
    ↓
logic.systems
    ↓
logic.models + logic.definitions

logic.content
    → carga definiciones y guardados
    → no depende de client
```

Esto evita que la lógica dependa de Pygame y permite probarla sin abrir una ventana.
