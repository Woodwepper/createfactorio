# Contexto del proyecto: simulador de fábricas

> Documento de continuidad. Actualizarlo cuando cambien decisiones importantes.
>
> Última revisión: 2026-08-30

## 1. Idea general

El proyecto es un simulador de fábricas para un jugador, inspirado visualmente en **Create** y conceptualmente en ideas de **Factorio**, además de decisiones propias.

El jugador administra el mundo desde una vista general. Controla los recursos, las construcciones, las fábricas y todo lo que ocurre dentro de ellas.

El ciclo general previsto es:

```text
recibir recursos iniciales
→ construir elementos básicos
→ crear fuentes de SU
→ localizar nodos de recursos
→ construir minas
→ colocar máquinas
→ extraer recursos
→ transportar recursos a fábricas
→ procesarlos mediante recetas
→ ampliar la infraestructura
```

El juego tendrá, como mínimo, dos modos:

- **Supervivencia:** el jugador debe conseguir y producir los recursos.
- **Creativo:** el jugador puede construir y obtener elementos libremente.

El juego será de un jugador por ahora. El multijugador y la existencia de jugadores dentro del mapa quedan fuera del alcance inmediato.

La plantilla de definiciones será editable. Se prevén dos formas de modificarla:

- editar los JSON directamente;
- utilizar posteriormente un editor dentro del juego.

El editor visual no forma parte del primer prototipo.

---

## 2. Alcance actual

No se va a borrar el proyecto actual ni se hará una refactorización masiva inmediata.

El código actual se considera un prototipo de referencia. La nueva dirección se implementará de forma incremental, conservando lo que sea reutilizable y reemplazando solamente las partes que impidan avanzar.

El primer prototipo funcional debe incluir las mecánicas principales discutidas:

```text
crear una fábrica
→ crear un módulo
→ asignar una receta
→ insertar una máquina
→ comprobar SU
→ comprobar inputs
→ crear una tarea
→ ejecutar ticks
→ completar la tarea
→ guardar output en buffer
→ entregar output al inventario
```

Quedan fuera del primer flujo jugable:

- mapa procedural completo;
- multijugador;
- editor visual;
- sistemas de jugadores dentro del mapa.

Los guardados, la capacidad de inventario y las definiciones JSON siguen siendo parte importante del proyecto, pero se implementarán después del núcleo mínimo de producción o en un flujo separado si complican demasiado el prototipo.

---

## 3. Arquitectura general

La arquitectura utiliza la separación:

```text
Definition = datos estáticos del juego
Model/Instance = estado vivo de una partida
```

Las definiciones describen lo que puede existir durante una partida. Las instancias representan el estado actual de objetos concretos.

La jerarquía principal es:

```text
World
└── Factory
    ├── Factory Inventory
    ├── SU Producers / redes de SU
    └── Modules
        └── Machines
            └── MachineTask / receta activa
```

Responsabilidades principales:

### `World`

- Representa el mundo de una partida.
- Contiene fábricas, nodos y otros objetos vivos.
- Utiliza `GameDefinitions` para resolver definiciones.
- No debe duplicar las definiciones completas dentro de cada instancia.
- Es un contenedor de estado; no controla directamente el reloj de la simulación.

### `Simulation`

Es el orquestador externo de ticks.

- Procesa las órdenes pendientes del jugador al inicio de cada tick.
- Coordina la actualización de sistemas globales.
- Actualiza redes de SU, construcciones, minería, producción y transportes en un orden definido.
- Registra resultados y eventos del tick.

### `Factory`

Es el coordinador local de su inventario, módulos y producción.

- Posee el inventario compartido de la fábrica.
- Contiene módulos.
- Conoce las redes de SU conectadas.
- Actualiza productores de SU que necesiten combustible.
- Calcula la capacidad de SU disponible.
- Calcula el SU requerido por todas las máquinas colocadas.
- Decide si la fábrica puede continuar trabajando.
- Coordina la planificación, asignación y entrega de producción.
- Actualiza su propio estado.

### `Module`

Coordina las máquinas que contiene.

- Tiene una receta asignada.
- Controla máquinas compatibles.
- Selecciona máquinas por eficiencia.
- Crea planes de producción.
- Asigna las tareas a sus máquinas.
- Actualiza su estado de producción.
- Utiliza el inventario de la fábrica, no un inventario propio.

### `Machine`

Es una instancia viva creada a partir de una definición de máquina.

- Tiene estado y progreso.
- Tiene una tarea activa y posiblemente tareas en cola.
- Mantiene buffers de input y output.
- Procesa como máximo un tick por llamada a `update()`.
- No debe consultar por su cuenta todo el mundo ni buscar definiciones en los registros.

### `MachineTask`

Representa una orden concreta para una máquina.

Contiene actualmente o debe contener conceptualmente:

- receta;
- inputs reservados para la tarea;
- cantidad de ciclos;
- identificador de la máquina a la que corresponde, o una relación explícita equivalente.

No se debe depender únicamente de que dos listas tengan el mismo orden para relacionar máquina y tarea.

---

## 4. Definiciones existentes

| Definición | Representa | Instancia relacionada |
|---|---|---|
| `ItemDefinition` | Un tipo de item, su nombre, categoría, stack size y posible entidad asociada | Item dentro de un inventario o stack |
| `MachineDefinition` | Características estáticas de una máquina: SU requerido, ciclos máximos, etc. | `Machine` |
| `RecipeDefinition` | Inputs, outputs, máquina requerida, duración y posibilidad de craft manual | `MachineTask` usa esta definición |
| `ModuleDefinition` | Identidad y niveles disponibles de un tipo de módulo | `Module` |
| `ModuleLevel` | Espacios de máquina y requisitos de un nivel | Estado `current_level` de `Module` |
| `FactoryDefinition` | Slots base y mejoras disponibles para una fábrica | `Factory` |
| `FactoryUpgrade` | Requisitos y nuevos slots de una mejora de fábrica | Nivel de `Factory` |
| `ResourceNodeDefinition` | Tipo, cantidad, regeneración e infinitud de un nodo | `ResourceNode` |
| `SuProducerDefinition` | Producción de SU, combustible e intervalo de combustible | `SuProducer` |
| `ResourceRequirement` | Referencia a un item y una cantidad dentro de recetas o costes | No es una instancia viva independiente |

Las definiciones se cargan desde JSON y se convierten en objetos mediante `from_dict()`.

Todas las definiciones deberían poder serializarse con `to_dict()`.

---

## 5. Registros y definiciones del juego

Los registros contienen únicamente definiciones estáticas:

- `item_registry`;
- `machine_registry`;
- `recipe_registry`;
- `module_registry`;
- `node_registry`;
- `su_producer_registry`.

Los registros se limpian y se vuelven a cargar al iniciar una partida nueva con otra plantilla. No deben contener instancias vivas.

Los identificadores son únicos en todo el juego. No debe haber dos definiciones con el mismo `id`.

El flujo previsto de carga es:

```text
JSON
↓
JsonLoader
↓
diccionarios crudos
↓
DefinitionParser
↓
objetos Definition
↓
DefinitionValidator
↓
registros
↓
GameDefinitions
↓
World
```

Responsabilidades:

### `JsonLoader`

- Buscar archivos de la plantilla.
- Leer JSON.
- Detectar errores de sintaxis o archivos faltantes.
- Resolver carpetas y anexos como `levels.json`.
- Devolver datos crudos y errores legibles.

### `DefinitionParser`

- Convertir diccionarios en objetos de definición.
- Usar `from_dict()`.
- Detectar campos ausentes o tipos incorrectos.
- Devolver objetos válidos y errores.

### `DefinitionValidator`

- Validar valores y referencias entre definiciones.
- Comprobar que existan los items usados por recetas y niveles.
- Comprobar que existan máquinas requeridas.
- Comprobar que los items que representan entidades apunten a definiciones existentes.
- Devolver errores acumulados.

### `GameDefinitions`

- Coordinar loader, parser y validator.
- Registrar definiciones si la carga es válida.
- Impedir la creación del mundo cuando existan errores críticos.
- Servir como fuente de definiciones para `World`.

Los errores se mostrarán tanto en modo desarrollador/consola como en la interfaz cuando exista.

Un guardado que utilice un `definition_id` inexistente o incompatible con la plantilla debe impedir la carga del mundo y mostrar un error legible.

---

## 6. Mundo y guardados

Una partida nueva se crea usando una plantilla completa de `GameDefinitions`.

Un guardado contiene el estado de las instancias, no las definiciones completas.

Ejemplo conceptual:

```json
{
  "definition_id": "mechanical_press",
  "state": "working",
  "progress": 4
}
```

Al cargar un guardado:

```text
1. cargar la plantilla de definiciones
2. validar la plantilla
3. cargar el estado guardado
4. comprobar que cada definition_id existe
5. reconstruir las instancias vivas
6. conectar cada instancia con su definición
7. crear el World
```

Las instancias deben conservar referencias a sus definiciones en memoria, pero el guardado debe almacenar principalmente sus identificadores y estado mutable.

El estado mutable incluye, según la instancia:

- nivel actual;
- máquinas colocadas;
- progreso;
- estado de máquinas y módulos;
- tareas activas o en cola;
- buffers;
- inventarios;
- estado de nodos y productores.

---

## 7. Inventarios y almacenamiento

El sistema de inventarios debe inspirarse en Minecraft y utilizar slots desde el inicio.

Un inventario conceptualmente contiene stacks:

```text
slot 0: iron_ingot x32
slot 1: coal x12
slot 2: mechanical_press x1
```

Reglas previstas:

- Los items se apilan si son del mismo tipo.
- Los items con datos especiales solo se apilan si sus datos son equivalentes.
- Los datos únicos de los items existen desde la primera versión; no se posponen como una simplificación del inventario.
- Un `ItemStack` contiene conceptualmente `item_id`, `amount` y datos opcionales. Los datos permiten representar tiers de máquina, configuración de contenedores u otras variantes sin impedir que los stacks equivalentes se apilen.
- `ItemDefinition.stack_size` determina el límite del stack.
- Un item máquina es inicialmente un item dentro de un inventario.
- Cuando se coloca en un módulo, se busca su definición y se crea una `Machine` viva.
- El item colocado se consume del inventario correspondiente.

Debe existir una clase de inventario general con operaciones como:

```text
add_item
consume
contains
get_quantity
can_add
copy
```

`PlayerInventory` y el inventario de la fábrica pueden compartir una base común, pero tener capacidades diferentes.

La fábrica posee un inventario compartido por sus módulos. No existe un inventario independiente por módulo.

La capacidad de almacenamiento de la fábrica podrá ampliarse mediante construcciones especializadas dedicadas a almacenar y administrar items.

Decisión de comportamiento recomendada:

- consultas como `contains`, `can_add` y `get_quantity` devuelven valores informativos;
- operaciones mutables como `consume` y `add_item` deben mantener las reglas del inventario;
- consumir más de lo disponible no debe producir una reducción parcial silenciosa;
- inicialmente puede usarse `RuntimeError`, pero posteriormente sería mejor una excepción específica como `InventoryError`.

Los métodos que expongan el contenido deben devolver copias para evitar modificaciones externas accidentales.

---

## 8. Recetas, ciclos y tareas

`RecipeDefinition.craft_time` representa el tiempo de completar la receta en ticks.

Por ahora una receta requiere un único tipo de máquina mediante `required_machine`.

Una receta puede:

- tener inputs;
- no tener inputs;
- tener outputs;
- no tener outputs;
- ser manual si `manual_crafting` está habilitado.

Las cantidades deben ser válidas y no negativas. Los items de inputs y outputs deben existir en los registros.

`MachineDefinition.cycles_per_craft` representa la cantidad máxima de ciclos que una máquina puede procesar al mismo tiempo dentro de una tarea.

`MachineTask.cycles` representa la cantidad concreta de ciclos asignados en esa tarea.

Ejemplo:

```text
Receta:
    input: iron_ingot x2
    output: steel_plate x1
    craft_time: 10 ticks

Máquina:
    cycles_per_craft: 3

Tarea:
    cycles: 3
    inputs: iron_ingot x6
    outputs: steel_plate x3
    duración: 10 ticks
```

Por ahora varios ciclos agrupados tardan lo mismo que una ejecución de la tarea. Esta decisión puede revisarse si el balance del juego lo requiere.

---

## 9. Estados de las máquinas

Estados lógicos previstos:

- `READY`: máquina activa, con SU disponible y lista para trabajar.
- `WORKING`: está procesando su tarea actual.
- `WAITING_DELIVERY`: terminó, pero conserva el output hasta que sea recogido.
- `OVERSTRESSED`: representación visual de una situación de sobrecarga; no debe ser la fuente principal de la lógica.

Transición prevista:

```text
READY
→ WORKING
→ WAITING_DELIVERY
→ READY
```

Al asignar una tarea:

- se consumen los inputs del inventario real;
- los inputs pasan al `input_buffer` de la máquina;
- la máquina inicia con progreso `0`;
- no debe avanzar más de un tick durante esa misma operación.

Mientras trabaja, la máquina no conserva nuevos inputs externos. Procesa una tarea activa a la vez y puede tener como máximo diez tareas pendientes en cola.

Cuando completa la tarea:

- genera outputs multiplicados por `cycles`;
- los coloca en `output_buffer`;
- pasa a `WAITING_DELIVERY`;
- no vuelve a `READY` hasta que los outputs hayan sido entregados.

El buffer de la máquina no tiene límite de espacio por ahora.

---

## 10. Planificación del módulo

El módulo crea un objeto de plan, no una única tarea aislada.

El plan debe relacionar cada máquina con su `MachineTask` mediante un identificador o una estructura explícita.

Proceso previsto:

```text
1. comprobar que hay receta
2. obtener máquinas compatibles
3. obtener máquinas READY
4. ordenar por eficiencia
5. crear una copia temporal del inventario
6. calcular ciclos posibles por máquina
7. crear tareas para las máquinas que puedan trabajar
8. descontar inputs solamente de la copia temporal
9. asignar el plan a las máquinas
```

La planificación no modifica el inventario real.

La copia temporal existe para reservar recursos durante la planificación de varias máquinas.

Si los recursos no alcanzan para todas las máquinas:

- las máquinas más eficientes tienen prioridad;
- se asignan primero las tareas de mayor eficiencia;
- el resto de los recursos permanece en el inventario;
- los empates de eficiencia se resuelven aleatoriamente.

Una máquina compatible que esté trabajando o esperando entrega no puede recibir una tarea activa nueva, aunque puede tener una tarea en cola si el sistema de cola ya está habilitado.

El módulo no puede insertar una máquina antes de tener una receta asignada.

Si se cambia la receta:

1. se advierte al jugador;
2. las máquinas incompatibles se retiran;
3. se pierde su progreso actual;
4. las máquinas retiradas se transfieren al inventario del jugador.

Estados de módulo previstos:

- `NO_RECIPE`;
- `MISSING_INPUTS`;
- `NO_MACHINES`;
- `NO_COMPATIBLE_MACHINES`;
- `PRODUCING_PARTIALLY`;
- `PRODUCING_FULLY`.

`NO_AVAILABLE_MACHINES` se eliminó.

Los estados de SU no pertenecen a la lógica interna del módulo; la sobrecarga es una condición global de la fábrica, aunque puede reflejarse visualmente en módulos y máquinas.

---

## 11. Redes de SU y actualización

El SU funciona como una capacidad compartida por tick, no como un item que se consume.

Una red de SU se compone de productores, consumidores y un hub de gestión. Las conexiones son abstractas en la primera versión. Productores y consumidores pueden conectarse al hub y también entre sí; todos los elementos conectados pertenecen a la misma red lógica.

Reglas confirmadas:

- el SU disponible es la suma de los productores conectados a una red;
- los productores pueden requerir combustible o ser pasivos;
- un consumidor de SU es una construcción completa, como una fábrica, mina, almacén especializado o infraestructura ferroviaria;
- cada consumidor necesita recibir toda su demanda para funcionar; no existe operación parcial;
- los consumidores se alimentan por prioridad, no mediante una comprobación binaria de toda la fábrica;
- la prioridad es híbrida: prioridad base del tipo de construcción más ajuste manual del jugador;
- si una red no alcanza para todos, continúan los consumidores prioritarios y se pausan los demás;
- el cálculo y la distribución se actualizan por tick;
- cuando vuelve a haber capacidad, los consumidores afectados pueden continuar automáticamente.

El tick es un orquestador. Las instancias tienen sus propios métodos `update()`, y esos métodos también pueden coordinar operaciones internas.

Orden provisional de actualización de una red:

```text
1. actualizar productores que requieren combustible
2. sumar SU producido por la red conectada
3. ordenar consumidores por prioridad
4. asignar SU completo a los consumidores prioritarios
5. pausar consumidores que no reciban su demanda completa
6. actualizar estados visuales de alimentación o sobrecarga
```

La fábrica conserva la autoridad sobre su inventario y la coordinación de módulos. La máquina recibe inputs ya validados y reservados al recibir una tarea; no busca ni administra por sí sola el inventario completo de la fábrica.

---

## 12. Estado actual del repositorio

Estructura relevante actual:

```text
game/logic/definitions/
    factory_definition.py
    game_definitions.py
    item_definition.py
    machine_definition.py
    module_definition.py
    module_level.py
    recipe_definition.py
    resource_node_definition.py
    resource_requirement.py
    su_producer_definition.py

game/logic/models/
    factory.py
    inventory.py
    machine.py
    machine_task.py
    module.py
    player_inventory.py
    resource_node.py
    su_producer.py

game/logic/managers/
    definition_parser.py
    json_loader.py

game/logic/systems/
    crafting_system.py

registries.py
main.py
```

Partes existentes:

- definiciones con `to_dict()` y `from_dict()`;
- registros globales;
- `Machine`, `MachineTask`, `Module`, `Factory` e inventarios;
- estados de máquinas, módulos, fábricas y productores;
- plantilla JSON inicial;
- spritesheets de ejemplo para la máquina `mechanical_press`.

Problemas conocidos del prototipo actual que no deben provocar una refactorización completa inmediata:

- `Factory.update()` todavía no implementa el flujo global;
- la planificación del módulo necesita alinearse con el nuevo objeto de plan;
- el cálculo de ciclos debe usar cantidades numéricas del inventario, no un booleano de `contains()`;
- la máquina todavía debe integrar correctamente progreso, ciclos, outputs y cola;
- la relación entre una máquina y su tarea debe hacerse explícita;
- el sistema de inventario actual utiliza diccionarios y debe evolucionar a slots;
- `JsonLoader`, `DefinitionParser` y `GameDefinitions` todavía requieren integración completa;
- el guardado y la reconstrucción del mundo todavía no están implementados.

Estos problemas se resolverán de forma incremental, no mediante una reescritura total del proyecto.

---

## 13. Próximo objetivo

El primer hito será un vertical slice visual y jugable, no un prototipo exclusivo de consola.

Debe incluir una ventana modesta pero funcional con:

```text
mapa placeholder
→ nodos de recursos visibles
→ inventario abrible
→ colocación de minas, fábricas y hubs de SU
→ conexiones abstractas de productores y consumidores
→ belts simples
→ módulos, máquinas y recetas
→ contenedores en fábricas
→ ticks visibles
```

El hito completo debe implementarse por capas pequeñas y comprobables:

1. ventana Pygame-ce y mapa placeholder;
2. cuadrícula, selección y colocación básica;
3. items con datos únicos, slots y contenedores;
4. fábricas, minas, módulos, máquinas y recetas;
5. tick, tareas, buffers y entrega de outputs;
6. productores, hubs y redes de SU priorizadas;
7. belts simples y transferencia visible;
8. interfaz básica para inventario, construcción y estado;
9. nodos de recursos y extracción.

Pygame-ce y pygame_gui serán la base del cliente. La lógica del juego debe seguir siendo independiente de Pygame.

Los belts simples son lineales entre un punto A y un punto B. Los items viajan visualmente y, si el destino no puede recibirlos, permanecen dentro del belt en vez de desaparecer; no existen bifurcaciones ni conexiones entre belts en la primera versión.

El cargador JSON, los guardados completos, trenes, portales y generación procedural se integrarán después de validar este vertical slice.

---

## 14. Órdenes del jugador y relación con la UI

La UI no modifica directamente el `World`. Cada acción del jugador se traduce en una orden con datos simples e identificadores.

```text
evento de UI
→ crear orden
→ añadir a cola de órdenes
→ esperar al siguiente tick
→ Simulation procesa la orden
→ el sistema correspondiente modifica el World
→ crear resultado
→ registrar resultado o evento
```

Las órdenes expresan una intención del jugador, no contienen la lógica de ejecución. Ejemplos futuros:

- crear una fábrica o mina;
- colocar un hub de SU;
- conectar productor y consumidor;
- colocar un belt;
- asignar una receta;
- insertar una máquina;
- añadir o retirar un contenedor.

Reglas del sistema de órdenes:

- una orden usa un `order_id`, datos simples, identificadores de entidades, tick de creación y prioridad;
- no contiene referencias directas a objetos vivos;
- `Simulation` procesa las órdenes al inicio del tick;
- las órdenes se ordenan por prioridad y, en empate, por orden de llegada;
- se procesan secuencialmente sobre el estado resultante de las órdenes anteriores del mismo tick;
- una orden inválida no detiene la simulación ni se reintenta automáticamente;
- cada orden genera un `OrderResult` legible;
- `GameLog` conserva historial de órdenes, resultados y eventos generales;
- el sistema que posee la regla ejecuta la orden: `OrderSystem` despacha, pero no implementa por sí mismo construcción, producción, minería o SU.

Este modelo separa la interfaz de la lógica y permite que una misma acción se origine desde UI, consola, pruebas o guardados sin duplicar reglas.

---

## 15. Forma de trabajo preferida

La ayuda debe ser profesional, didáctica y clara, sin excesiva informalidad.

El usuario prefiere un enfoque de mentor para aprender y tomar decisiones:

- hacer preguntas antes de implementar cuando el diseño sea ambiguo;
- ofrecer pistas y pseudocódigo;
- explicar el motivo de cada decisión;
- no reescribir código sin solicitarlo explícitamente;
- revisar primero lo que ya existe;
- evitar solicitar demasiadas acciones o cambios a la vez;
- mantener cada sesión enfocada en un objetivo pequeño.

Al retomar el proyecto, comenzar por leer este archivo y resumir únicamente:

1. dónde se quedó el desarrollo;
2. qué decisiones están confirmadas;
3. qué problemas están pendientes;
4. cuál es el siguiente paso pequeño.

---

## 16. Cierre de la sesión actual

Fecha de referencia: 2026-09-03.

### Trabajo realizado hoy

- Se definió y creó una estructura estable para el proyecto:
  - `game/logic/core` para `World` y `Simulation`;
  - `game/logic/orders` para órdenes y resultados;
  - `game/logic/content` para carga y validación futura;
  - `client/scenes`, `client/ui`, `client/rendering` y `client/interaction`;
  - `data/templates` y `data/saves`;
  - `tests/unit` y `tests/integration`.
- Se añadieron los paquetes Python y sus `__init__.py` básicos.
- Se creó una ventana funcional con `pygame-ce` en modo ventana.
- Se implementó el bucle de Pygame con eventos, FPS y cierre seguro.
- `World` mantiene un contador de ticks.
- `Simulation` decide si el mundo avanza.
- Se implementó `SimulationClock` para velocidades de simulación.
- Se añadieron velocidades de `x1` a `x10` y pausa mediante botones.
- Se creó un HUD temporal con tick, FPS, estado, velocidad y tiempo acumulado.
- El HUD actualiza los FPS cada medio segundo.
- Se creó el contrato base de escenas con `handle_event()`, `update()` y `draw()`.
- Se creó `MainMenuScene` con botones de crear mundo, settings y salida.
- Se creó `WorldScene` con controles de pausa y velocidad.
- `App` ya puede cambiar de `MainMenuScene` a `WorldScene` al solicitar un mundo nuevo.
- Se integró en este contexto el sistema de órdenes del contexto remoto:
  - la UI expresa intenciones;
  - `Simulation` procesa órdenes en los ticks;
  - los sistemas aplican las reglas;
  - cada orden produce un resultado legible;
  - `GameLog` conserva eventos y resultados.

### Estado funcional actual

El flujo actual es:

```text
abrir aplicación
→ MainMenuScene
→ pulsar Create world
→ crear World y Simulation
→ cambiar a WorldScene
→ mostrar HUD
→ ejecutar ticks
→ pausar o cambiar velocidad
```

La aplicación y las escenas se validaron mediante compilación e imports. La ventana interactiva no se deja ejecutándose durante las comprobaciones automáticas.

### Pendientes inmediatos

- Ejecutar manualmente el flujo completo del menú y confirmar los botones en pantalla.
- Crear la cuadrícula placeholder.
- Integrar el primer mapa visual.
- Definir y crear el primer `CreateWorld` o `GameSession` de forma más formal si sigue siendo necesario.
- Implementar la primera orden real dentro de un mundo existente, probablemente `PlaceBuildingOrder`.
- Crear `ItemStack`, `Inventory` y `Container`.

### Nota de continuidad

El repositorio anterior se conserva como referencia histórica. El desarrollo activo se está reconstruyendo de forma incremental, manteniendo la separación entre lógica y cliente.
