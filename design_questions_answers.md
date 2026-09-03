# Preguntas y respuestas de diseño

Este documento conserva las decisiones obtenidas durante la conversación de diseño. No pretende ser una especificación definitiva: las decisiones marcadas como pendientes pueden cambiar durante el prototipo.

---

## 1. Visión del juego

### ¿Qué tipo de juego se está construyendo?

Un simulador de fábricas, proyecto personal inspirado visualmente en Create, conceptualmente en Factorio y en ideas propias.

### ¿Qué papel cumple el jugador?

El jugador administra el mundo desde una vista general. Controla sus fábricas, construcciones, recursos y todo lo que existe dentro de ellas.

### ¿Cuál es el ciclo principal?

```text
recursos iniciales
→ construcciones básicas
→ fuentes de SU
→ localizar nodos
→ construir minas
→ colocar máquinas
→ extraer recursos
→ enviar recursos a fábricas
→ producir mediante recetas
→ ampliar la infraestructura
```

### ¿Será un juego de un jugador?

Sí, por ahora. El multijugador y la existencia de jugadores dentro del mapa quedan fuera del primer alcance.

### ¿Habrá distintos modos de juego?

Sí:

- **Supervivencia:** el jugador debe conseguir los recursos.
- **Creativo:** el jugador puede construir y obtener elementos libremente.

### ¿Qué queda fuera del primer prototipo?

- mapa procedural completo;
- editor visual completo;
- multijugador;
- entidades de jugadores dentro del mapa.

El sistema de inventarios, las definiciones, la producción, el SU y los guardados son importantes, aunque se implementarán por etapas.

---

## 2. Definiciones, instancias y partidas

### ¿Qué diferencia hay entre definiciones y modelos?

Las definiciones son datos estáticos que describen lo que puede existir durante una partida.

Los modelos son instancias vivas que contienen el estado mutable de una partida.

Ejemplo:

```text
MachineDefinition:
    craft_time, SU requerido, ciclos permitidos

Machine:
    estado actual, progreso, tarea, buffers
```

### ¿Qué contienen los registros?

Los registros contienen únicamente definiciones estáticas:

- items;
- máquinas;
- recetas;
- módulos;
- fábricas;
- nodos de recursos;
- productores de SU.

No deben contener instancias vivas.

### ¿Cómo se reconstruye una instancia desde un guardado?

El guardado almacena el `definition_id` y el estado mutable. Al cargar:

```text
1. cargar la plantilla de definiciones
2. validar la plantilla
3. cargar el guardado
4. buscar cada definition_id
5. reconstruir la instancia viva
6. conectarla con su definición
7. crear el World
```

Si falta una definición o la plantilla no es coherente con el guardado, el mundo no debe cargar.

### ¿Qué debe contener el mundo?

El `World` contiene el estado de la partida: fábricas, nodos, inventarios, productores y demás instancias vivas.

El `World` debe utilizar `GameDefinitions` para resolver definiciones, en lugar de duplicarlas dentro de cada guardado.

---

## 3. Definiciones del juego

| Definición | Qué representa | Instancia o uso |
|---|---|---|
| `ItemDefinition` | Tipo de item, nombre, categoría, tamaño de stack y entidad asociada | Item o stack dentro de un inventario |
| `MachineDefinition` | Características estáticas de una máquina | `Machine` |
| `RecipeDefinition` | Inputs, outputs, duración, máquina requerida y craft manual | `MachineTask` la utiliza |
| `ModuleDefinition` | Tipo de módulo y niveles disponibles | `Module` |
| `ModuleLevel` | Slots de máquina y requisitos de un nivel | Estado de nivel del `Module` |
| `FactoryDefinition` | Slots base y mejoras de una fábrica | `Factory` |
| `FactoryUpgrade` | Requisitos y nuevos slots de una mejora | Mejora de `Factory` |
| `ResourceNodeDefinition` | Cantidad, regeneración e infinitud de un nodo | `ResourceNode` |
| `SuProducerDefinition` | Producción de SU, combustible e intervalos | `SuProducer` |
| `ResourceRequirement` | Referencia a un item y una cantidad | Inputs, outputs y costes |

Todas las definiciones deben poder convertirse desde y hacia diccionarios mediante `from_dict()` y `to_dict()`.

---

## 4. Items e inventarios

### ¿Cómo se representa actualmente un inventario?

Actualmente se utilizaban diccionarios, pero se decidió evolucionar a un sistema de slots inspirado en Minecraft.

### ¿Cómo funcionarán los slots?

Conceptualmente:

```text
slot 0: iron_ingot x32
slot 1: coal x12
slot 2: mechanical_press x1
```

### ¿Cuándo pueden apilarse dos items?

Se pueden apilar si son del mismo tipo. Si tienen datos especiales, esos datos también deben ser equivalentes.

El `stack_size` de `ItemDefinition` define el máximo de un stack.

### ¿Cómo se representa una máquina como item?

Una máquina existe inicialmente como un item. Cuando el jugador la coloca en un módulo:

```text
item_id del inventario
→ buscar ItemDefinition
→ buscar MachineDefinition
→ crear Machine viva
→ consumir el item
```

Una máquina viva no se crea normalmente fuera del módulo que la recibe.

### ¿Habrá capacidad de inventario?

Sí. El inventario debe usar slots desde el inicio.

El inventario de la fábrica tendrá capacidad propia y podrá ampliarse mediante construcciones especializadas para almacenar y administrar items.

El inventario del jugador y el de la fábrica pueden compartir una clase base, pero tener capacidades diferentes.

### ¿Qué operaciones debe ofrecer el inventario?

```text
add_item
consume
contains
get_quantity
can_add
copy
```

### ¿Qué debe hacer `consume()` si faltan items?

La decisión conceptual es que no debe consumir parcialmente de forma silenciosa. Debe fallar mediante una excepción de inventario o, inicialmente, mediante `RuntimeError`.

Los métodos de consulta deben devolver información. Los métodos mutables deben mantener las reglas del inventario.

Los métodos que devuelvan el contenido deben entregar una copia, no el diccionario interno.

---

## 5. Recetas

### ¿Qué significa `craft_time`?

Es el tiempo que tarda una receta en completarse y está expresado en ticks.

### ¿Cuántas máquinas puede requerir una receta?

Por ahora una receta requiere un único tipo de máquina.

### ¿Puede una receta ser manual?

Sí. `manual_crafting` indica que el jugador puede crearla sin depender de una fábrica o de procesos complejos.

### ¿Puede una receta tener cero inputs o cero outputs?

Sí, ambas posibilidades deben ser válidas.

### ¿Se permiten cantidades inválidas?

No. Las cantidades deben validarse para impedir valores negativos o inválidos.

### ¿Deben validarse los outputs?

Sí. Los items de inputs y outputs deben existir en los registros.

---

## 6. Máquinas y tareas

### ¿Qué significa `cycles_per_craft`?

Es la cantidad de ciclos de una receta que la máquina puede realizar al mismo tiempo dentro de una tarea.

### ¿Qué significa `MachineTask.cycles`?

Es la cantidad de ciclos concretos que se repiten dentro de esa tarea. Una tarea puede contener uno o más ciclos.

Ejemplo:

```text
Receta:
    iron_ingot x2 → steel_plate x1

Tarea:
    cycles = 3
    inputs = iron_ingot x6
    outputs = steel_plate x3
```

Los inputs y outputs se multiplican por la cantidad de ciclos.

Los ciclos agrupados utilizan el tiempo definido para la tarea; esta decisión puede revisarse al balancear el juego.

### ¿Qué estados tiene una máquina?

- `READY`: activa, con SU suficiente y lista para trabajar.
- `WORKING`: completando una tarea.
- `WAITING_DELIVERY`: terminó y espera la recogida del output.
- `OVERSTRESSED`: estado principalmente visual para representar sobrecarga.

### ¿Puede una máquina tener cola?

Sí. Puede tener una tarea activa y tareas pendientes en cola, pero procesa una sola tarea activa a la vez.

### ¿Cuándo se consumen los inputs?

Al recibir la tarea. Los inputs se retiran del inventario de la fábrica y pasan al buffer de la máquina.

La implementación debe conservar la fábrica como autoridad del inventario real: el módulo planifica y la fábrica confirma el consumo; la máquina recibe los inputs ya validados al asignarse la tarea.

### ¿Qué ocurre al terminar una tarea?

```text
WORKING
→ output_buffer
→ WAITING_DELIVERY
→ entrega confirmada
→ READY
```

La máquina no vuelve a `READY` hasta que el output haya sido retirado.

El buffer no tiene límite de espacio por ahora.

### ¿Qué hace `Machine.update()`?

Procesa como máximo un tick. No devuelve necesariamente una tarea ni consulta directamente todo el inventario de la fábrica.

---

## 7. Módulos y planificación

### ¿Qué hace `Module`?

- contiene máquinas;
- tiene una receta asignada;
- identifica máquinas compatibles;
- selecciona máquinas eficientes;
- planifica tareas;
- actualiza su estado.

### ¿Qué devuelve la planificación?

Un objeto de plan que relaciona cada tarea con el identificador de la máquina correspondiente.

No se debe depender únicamente del orden de dos listas para relacionarlas.

### ¿La planificación consume el inventario real?

No. Utiliza una copia temporal del inventario para simular reservas entre máquinas.

Proceso:

```text
crear copia temporal
→ calcular ciclos por máquina
→ crear MachineTask
→ descontar solo de la copia
→ devolver el plan
→ la fábrica confirma y consume el inventario real
```

### ¿Cómo se priorizan las máquinas?

- primero se ordenan por eficiencia;
- las más eficientes reciben recursos primero;
- los recursos restantes permanecen en el inventario;
- los empates se resuelven aleatoriamente.

### ¿Cuándo se puede insertar una máquina?

No se puede insertar antes de asignar una receta al módulo.

Si la receta cambia y una máquina deja de ser compatible:

1. se advierte al jugador;
2. se retira la máquina;
3. se pierde su progreso;
4. se transfiere el item al inventario del jugador.

### ¿Qué estados tiene un módulo?

- `NO_RECIPE`;
- `MISSING_INPUTS`;
- `NO_MACHINES`;
- `NO_COMPATIBLE_MACHINES`;
- `PRODUCING_PARTIALLY`;
- `PRODUCING_FULLY`.

El estado `NO_AVAILABLE_MACHINES` se eliminó.

Los estados de SU no pertenecen a la lógica principal del módulo, aunque pueden reflejarse visualmente.

---

## 8. Fábrica y SU

### ¿Qué responsabilidad tiene `Factory`?

Es el orquestador de alto nivel. Administra:

- inventario compartido;
- módulos;
- redes de SU conectadas;
- productores de SU;
- consumo y entrega de recursos;
- actualización de máquinas y módulos;
- estados globales.

### ¿Cómo se calcula el SU?

La fábrica recibe capacidad de las redes de SU que tiene conectadas.

El SU requerido es la suma del `su_required` de todas sus máquinas colocadas.

Las máquinas consumen capacidad aunque estén:

- `READY`;
- `WORKING`;
- `WAITING_DELIVERY`.

La capacidad se actualiza por tick y no es un item que se consuma.

### ¿Qué ocurre si falta SU?

Se detienen las actualizaciones de máquinas y módulos. Sus progresos se conservan.

Los productores que necesitan combustible continúan actualizándose. Los productores pasivos no necesitan una actualización activa para aportar su capacidad.

Cuando vuelve a haber SU suficiente, la fábrica continúa automáticamente en el mismo tick en que comprueba que la capacidad es suficiente.

### ¿Cuál es el orden provisional de `Factory.update()`?

```text
1. actualizar productores de SU que necesiten combustible
2. calcular capacidad de las redes conectadas
3. calcular SU requerido
4. si falta SU, detener máquinas y módulos
5. entregar outputs pendientes cuando sea posible
6. pedir planes a los módulos
7. consumir inputs reales
8. asignar tareas
9. actualizar máquinas
10. actualizar estados
```

El tick es un orquestador. Los métodos `update()` de las instancias coordinan sus propias operaciones internas.

---

## 9. JSON, validación y registros

### ¿Cuál es el flujo de carga?

```text
JSON
→ JsonLoader
→ datos crudos
→ DefinitionParser
→ objetos Definition
→ DefinitionValidator
→ registros
→ GameDefinitions
→ World
```

### ¿Qué hace cada etapa?

- `JsonLoader`: lee archivos y detecta errores de formato o de sistema de archivos.
- `DefinitionParser`: convierte diccionarios en objetos de definición.
- `DefinitionValidator`: valida valores y referencias entre definiciones.
- `GameDefinitions`: coordina el proceso y registra definiciones válidas.

### ¿Cómo se manejan los errores?

Primero se verifica que el JSON tenga una estructura válida. Si no la tiene, se informa y no continúa con ese proceso.

Si la estructura tiene sentido, se realiza la validación semántica. Los errores se acumulan y se muestran juntos.

Los errores deben poder mostrarse:

- en consola para modo desarrollador;
- en la interfaz para que el jugador pueda entender qué ocurre.

Los errores críticos impiden crear o cargar el mundo. Los errores no críticos podrán evaluarse individualmente más adelante.

---

## 10. Decisión de reinicio

El proyecto anterior se conserva únicamente como archivo histórico.

El nuevo proyecto comenzará desde cero conceptualmente, pero no se hará una refactorización masiva del código antiguo porque ya no es necesario conservarlo en la carpeta de trabajo.

La nueva implementación debe comenzar con un prototipo vertical pequeño:

```text
Inventory por slots
→ Factory
→ Module
→ Machine compatible
→ RecipeDefinition
→ MachineTask
→ consumo de inputs
→ ticks
→ output buffer
→ entrega al inventario
→ estados correctos
```

El desarrollo debe avanzar por capas pequeñas y comprobables.
