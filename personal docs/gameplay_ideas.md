# Lluvia de ideas: diseño y gameplay

Este documento reúne ideas de gameplay. No todas son decisiones definitivas.

Estados usados:

- **Confirmado:** dirección acordada actualmente.
- **Por explorar:** idea atractiva que necesita diseño.
- **Pendiente de resolver:** existe una pregunta o una contradicción relevante.
- **Evitar:** dirección que no encaja con la visión del juego.

---

## 1. Fantasía principal

### Confirmado

El objetivo emocional del juego es que el jugador pueda mirar su mundo y sentir que creó:

```text
un ecosistema industrial completo,
estructurado,
animado,
visible y vivo.
```

La estética debe inspirarse fuertemente en **Create**:

- maquinaria visible;
- movimiento mecánico;
- engranajes, vapor y sistemas industriales;
- construcciones decorativas;
- animaciones con spritesheets para ciertas máquinas y procesos;
- pixel art como base visual.

El jugador administra el mundo desde una perspectiva general, no controla un personaje individual.

---

## 2. Mundo y exploración

### Confirmado

- El mundo utiliza una cuadrícula.
- Debe tener estética pixel art.
- Tendrá distintas zonas, biomas y distribución variable de recursos.
- La generación procedural puede cambiar:
  - biomas;
  - ubicación de recursos;
  - características de los lugares;
  - posibles estructuras especiales.
- El jugador descubre nodos explorando visualmente el mapa.
- Los recursos serán una mezcla de:
  - infinitos;
  - finitos;
  - renovables;
  - no renovables.

### Por explorar: prospección

Algunos nodos no deberían aparecer visualmente al inicio.

Ejemplo principal:

```text
petróleo u otros recursos subterráneos
→ no visibles en el mapa
→ se descubren mediante construcciones,
   herramientas o mecánicas de prospección
```

Esto permite que la exploración no sea solo recorrer el mapa: el jugador debe desarrollar infraestructura para conocer mejor el mundo.

### Por explorar: estructuras del mundo

El mundo podría contener estructuras, ruinas o sectores industriales recuperables.

Posibles funciones:

- ofrecer recursos o máquinas iniciales;
- desbloquear una zona reutilizable;
- servir como proyecto de restauración;
- actuar como punto de partida para una nueva industria.

---

## 3. Recursos y cadenas de producción

### Confirmado

Se quieren recursos naturales y artificiales, inspirados parcialmente en Minecraft:

- madera;
- minerales;
- combustibles;
- recursos poco comunes;
- componentes industriales;
- materiales procesados;
- posibles fluidos como petróleo.

Las cadenas de producción deben poder crecer hasta requerir sectores propios de industria.

Ejemplo conceptual:

```text
recursos crudos
→ materiales procesados
→ componentes
→ maquinaria / infraestructura / productos avanzados
```

El desafío debe provenir de una combinación de:

- falta de inputs;
- almacenamiento lleno;
- SU insuficiente;
- distancias entre recursos e industrias;
- transporte;
- distribución del mundo;
- cadenas productivas más complejas.

### Por explorar: subproductos y reciclaje

Se quiere incluir subproductos, residuos o reciclaje de alguna forma.

Posibles direcciones, todavía sin decidir:

```text
receta principal
→ producto principal
+ subproducto útil

residuo
→ reciclaje
→ recurso secundario

material imperfecto
→ procesado adicional
→ componente aprovechable
```

La intención no es castigar al jugador con basura obligatoria, sino crear rutas productivas, eficiencia y opciones de diseño.

---

## 4. Construcciones y sectores industriales

### Confirmado

### Fábricas

- Las fábricas contienen módulos.
- Los módulos contienen máquinas.
- Las fábricas procesan recursos mediante recetas.

### Minas

- Una mina es conceptualmente similar a una fábrica.
- Solo puede colocarse sobre nodos de recursos.
- También contiene módulos.
- Sus módulos requieren máquinas específicas, por ejemplo taladros.
- Esas máquinas consumen SU y extraen recursos del nodo.

### Fuentes de SU

- Pueden requerir combustible o ser pasivas.
- A cambio proporcionan capacidad de SU.

### Almacenes

Los almacenes son construcciones similares a fábricas y minas, pero dedicadas a contener y organizar recursos.

#### Estructura por contenedores

Un almacén no es simplemente un inventario gigante. El jugador coloca contenedores de carga dentro del edificio.

```text
Almacén
├── contenedor de items general
├── contenedor filtrado para un recurso
├── contenedor de fluidos
└── otros contenedores especializados
```

Los contenedores definen la capacidad y el tipo de recurso que puede almacenar el edificio.

Tipos previstos:

- contenedores generales para varios items;
- contenedores especializados en un único recurso;
- contenedores de fluidos;
- contenedores de carga que pueden transportarse mediante trenes adecuados.

#### Relación con fábricas y minas

- Las fábricas y minas también pueden alojar contenedores.
- Sus espacios de almacenamiento son menores que los de un almacén dedicado.
- El almacén permite aumentar capacidad sin convertir cada fábrica en un inventario enorme.
- Cada almacén es independiente; no existe una red global de almacenamiento compartido.

#### Relación con trenes

Los trenes pueden interactuar con contenedores de dos formas previstas:

```text
1. Extraer recursos de un contenedor y cargarlos en sus propios contenedores.
2. Transportar contenedores de carga completos cuando el tipo de tren lo permita.
```

Esto deja espacio para trenes especializados y logística visible.

#### Gestión inicial y futura

En una primera versión, el almacén se limita a almacenar recursos y ofrecer puntos de carga o descarga.

Más adelante puede incorporar gestión simple, sin convertirse en un sistema de programación complejo:

- aceptar o rechazar recursos;
- filtros por item o fluido;
- mínimos y máximos de stock;
- prioridades básicas de entrada o salida;
- estadísticas de cantidad, consumo y producción.

La logística inicial depende principalmente de los transportes, no de reglas automáticas de almacén.

### Trenes

Los trenes son una mecánica logística de final del early game y midgame.

Su función es mover grandes cantidades de items entre sectores distantes sin que el jugador deba hacerlo manualmente. El transporte tarda tiempo, viaja de forma visible y se configura mediante esquemas.

#### Infraestructura física

- Las vías existen físicamente sobre la cuadrícula.
- El jugador construye una conexión seleccionando dos puntos.
- El juego busca y crea automáticamente una ruta válida entre esos puntos.
- Más adelante la infraestructura puede incluir curvas, bifurcaciones, cruces, puentes, túneles y estaciones.
- Si un tren necesita compartir un tramo con otro, el sistema crea una vía adicional automáticamente; no se busca implementar señales o gestión de colisiones al inicio.
- Si una vía se elimina mientras un tren la está recorriendo, el tren se detiene.
- El jugador puede eliminar y rediseñar vías sin castigos permanentes.

#### Estaciones y esquemas

Las vías y los esquemas de los trenes son sistemas distintos:

```text
Vías = rutas físicas disponibles
Esquema = instrucciones de un tren
```

Un esquema mínimo contiene:

```text
estación A
→ cargar recursos
→ viajar a estación B
→ descargar recursos
→ volver a estación A
```

Con el tiempo, los esquemas pueden admitir varias paradas y condiciones configurables:

- cargar hasta llenar;
- cargar o descargar una cantidad concreta;
- esperar hasta que exista espacio en destino;
- esperar una condición de inventario;
- repetir la ruta.

Las rutas pueden configurarse manualmente. Más adelante también podrían existir rutas automáticas en función de demanda o stock.

#### Rol en la red logística

Los trenes pueden transportar items entre prácticamente cualquier construcción que produzca o consuma recursos:

- minas;
- fábricas;
- almacenes;
- estaciones logísticas;
- otros sectores industriales.

Los almacenes pueden funcionar como centros centralizados y estaciones ferroviarias.

#### Costes y especialización

Los trenes necesitan motores. Según el tipo de motor o tren, pueden:

- no requerir combustible;
- requerir combustible;
- requerir SU;
- requerir ambos;
- especializarse en capacidad, velocidad o tipo de carga.

El combustible y el SU deben crear decisiones de infraestructura, no mantenimiento tedioso.

#### Relación con otros transportes

- Los belts pueden servir para conexiones directas y más lentas.
- Los trenes son más apropiados para volumen y distancia.
- El endgame puede añadir portales o transporte cuántico.
- Los portales podrían requerir líquidos, recursos especiales o infraestructura compleja.
- El transporte cuántico puede escalar desde rápido hasta instantáneo.

#### Implementación por niveles

```text
Nivel 0:
Tren visual entre dos estaciones ficticias.

Nivel 1:
Un tren funcional A → B → A que carga y descarga items.

Nivel 2:
Estaciones con inventarios, condiciones de carga y almacenes centrales.

Nivel 3:
Esquemas con varias paradas y varias rutas.

Nivel 4:
Red ferroviaria con bifurcaciones, puentes, túneles y tipos de tren.

Nivel 5:
Motores, combustible, SU, logística automática y transporte de endgame.
```

### Sectores industriales: organización visual

Los sectores no son una mecánica de reglas, bonificaciones o límites.

Son una forma libre en la que el jugador puede organizar visualmente su mundo y sus propias metas industriales, por ejemplo:

```text
sector minero
sector de fundición
sector mecánico
sector logístico
sector de almacenamiento
sector energético
sector de componentes avanzados
```

El jugador puede separar industrias porque le resulta útil, atractivo o fácil de entender, pero el juego no debe imponer beneficios, penalizaciones ni restricciones por pertenecer a un sector.

Las cadenas complejas pueden llevar naturalmente a crear zonas separadas, sin convertir esos sectores en entidades de lógica.

---

## 5. Transporte y vida visual del mundo

### Confirmado

El juego debe verse vivo. Los recursos idealmente deben viajar de manera visible por el mapa.

Los trenes son una candidata principal para representar logística visible. También podrían existir otros transportes en etapas avanzadas.

### Pendiente de resolver: abstracción frente a representación

Todavía no está decidido qué conexiones deben verse físicamente y cuáles pueden ser abstractas.

Posible división inicial:

| Sistema | Posible representación |
|---|---|
| Máquinas dentro de módulos | Abstracta inicialmente |
| Transporte de items entre sectores | Visible, especialmente por trenes |
| Redes de SU | Abstractas con overlay visual o conexiones visibles simplificadas |
| Inputs y outputs de una máquina | Buffers internos abstractos |
| Almacenes y estaciones | Construcciones visibles |

La prioridad visual es importante, pero no debe volver el primer prototipo demasiado complejo.

### Belts simples

Los belts son transporte visible y lineal entre un punto A y un punto B.

```text
origen
→ belt
→ destino
```

Reglas de la primera versión:

- no tienen bifurcaciones;
- no se conectan directamente con otros belts;
- transportan items de forma visible;
- son más lentos que los trenes;
- si el destino no puede recibir un item, el item permanece dentro del belt;
- los items no desaparecen al bloquearse el destino;
- el belt puede acumular visualmente items en tránsito, como un sistema físico real.

---

## 6. Redes de SU

### Modelo confirmado: hub con distribución priorizada

Una red de SU tiene un **hub central** de gestión. Productores y consumidores pueden conectarse al hub y también conectarse entre sí de forma abstracta; todos los elementos conectados forman una misma red lógica.

```text
Productores de SU
↔ hub de red ↔ consumidores de SU
↕                 ↕
conexiones directas abstractas entre elementos de la red
```

Las fuentes de SU aportan capacidad; algunas consumen recursos y otras pueden ser pasivas.

La red suma la capacidad de todos los productores conectados y la distribuye entre consumidores según prioridad. No se detiene toda la fábrica cuando no alcanza para todos.

Ejemplo:

```text
Producción conectada:
4 ruedas de agua = 400 SU

Consumidores:
fábrica de hierro = 350 SU
fábrica de grava = 300 SU
```

Si la fábrica de hierro tiene mayor prioridad:

```text
400 SU disponibles
→ fábrica de hierro recibe 350 SU
→ quedan 50 SU
→ fábrica de grava no recibe SU suficiente y se detiene
```

La red mantiene activos los consumidores que puede sostener por prioridad, en lugar de paralizar todos los consumidores por falta de capacidad total.

Cada consumidor de SU es una construcción completa, por ejemplo una fábrica, mina, almacén especializado o infraestructura ferroviaria. Una construcción necesita recibir toda su demanda de SU para funcionar; no opera parcialmente.

La prioridad es híbrida:

```text
prioridad base del tipo de construcción
+ ajuste manual del jugador
```

### Actualización conceptual de una red

```text
1. actualizar productores que requieran combustible
2. sumar SU producido por productores conectados
3. ordenar consumidores conectados por prioridad
4. distribuir capacidad de mayor a menor prioridad
5. actualizar solo los consumidores alimentados
6. reflejar visualmente los consumidores sin SU
```

### Pendiente de resolver más adelante

- ¿Las conexiones al hub son visibles en el mapa, abstractas o una mezcla de ambas?
- ¿Una fábrica, mina, almacén o tren puede conectarse a más de una red de SU?

---

## 7. Progresión

### Confirmado

La progresión no debe sentirse como un árbol lineal obligatorio.

La filosofía es más cercana a Minecraft:

```text
todo puede existir desde el principio,
pero para usarlo el jugador debe descubrir recursos,
construir la infraestructura necesaria
y resolver sus propios problemas industriales.
```

El crecimiento permite:

- usar nuevas máquinas;
- descubrir nuevos materiales;
- obtener nuevas formas de conseguir recursos;
- ampliar espacio e infraestructura;
- mejorar transporte;
- aumentar eficiencia;
- escalar la producción.

### Por explorar

Pueden coexistir sistemas opcionales:

- quests no obligatorias;
- proyectos industriales;
- árboles de mejoras no lineales;
- restauración de estructuras;
- tecnologías o máquinas muy potentes pero complejas;
- grandes proyectos de infraestructura.

La regla es que estos sistemas deben dar dirección o posibilidades, no obligar al jugador a seguir una ruta única.

---

## 8. Metas de largo plazo

### Confirmado

El juego debe tener potencial prácticamente infinito.

No se busca una presión externa fija. La presión principal debe venir de los objetivos que el propio jugador decide asumir.

El jugador debería poder proponerse metas como:

```text
crear una fábrica totalmente automática
construir una red ferroviaria industrial
centralizar almacenamiento
producir grandes volúmenes de componentes
crear sectores especializados
optimizar una red de SU
construir una industria visualmente atractiva
restaurar y reutilizar zonas industriales
```

### Por explorar: proyectos industriales opcionales

Los proyectos grandes pueden dar objetivos concretos sin eliminar libertad.

Ejemplos:

```text
restaurar un sector industrial abandonado
construir una estación ferroviaria central
crear una planta de energía compleja
abrir una nueva zona de explotación
construir una máquina excepcionalmente potente
crear infraestructura para una industria avanzada
```

---

## 9. Libertad, errores y dificultad

### Confirmado

- El jugador debe poder deshacer sus decisiones.
- No se busca castigar con errores permanentes.
- La dificultad debe provenir de los sistemas y su organización, no de castigos arbitrarios.
- No se quiere presión externa obligatoria como tiempo, competencia o mantenimiento molesto.

### Evitar

- construir sin tener ningún objetivo propio o problema que resolver;
- progresión estrictamente lineal;
- tareas repetitivas que no añadan decisiones;
- errores irreversibles;
- mantenimiento impuesto solo para ocupar tiempo;
- sistemas complejos que no aporten creatividad o expresión industrial.

---

## 10. Temas pendientes para la siguiente ronda

### Almacenes

1. ¿El almacén debe aportar solo más slots, o también clasificación, filtros, prioridades y distribución?
2. ¿Puede funcionar como estación logística entre trenes y fábricas?
3. ¿Puede dar estadísticas de stock, consumo y producción?
4. ¿Debe permitir que el jugador establezca metas de stock?

### Sectores

1. ¿Qué obliga o incentiva al jugador a separar sectores, además de la estética?
2. ¿Distancia, transporte, eficiencia, capacidad de SU, contaminación, temperatura, ruido o espacio?
3. ¿Qué debería distinguir un sector eficiente de uno simplemente grande?

### Metas

1. ¿Quieres que los proyectos industriales tengan recompensas mecánicas, visuales o ambas?
2. ¿Las quests deben ser generadas por el mundo, escritas manualmente o creadas por el propio jugador?
3. ¿Qué objetivo te gustaría que tuviera una partida avanzada, sin que sea un final obligatorio?
