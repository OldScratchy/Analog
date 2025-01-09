# Analog! 🐿️

**Analog** es un proyecto de muestra para recolectar y visualizar logs en formatos estructurados o "clásicos" usando **Fluent Bit**, **Elasticsearch** y **Grafana**. Todo esto, permite analizar y monitorear logs fácilmente a través de dashboards preconfigurados.

---

## 🏗️ Infraestructura

**Analog**, tal como se presenta, utiliza una infraestructura basada en contenedores para recolectar, procesar y visualizar logs en los dos formatos mencionados. A continuación, se describen los servicios:

### 📥 Fluent Bit

**Fluent Bit** es un procesador y despachador de logs ligero y eficiente. En este proyecto, se utiliza para:

- Leer logs desde:
  - **Logs estructurados** generados en formato JSON.
  - **Logs clásicos** generados en formato de texto plano.
- Aplicar parsers para interpretar los formatos de log.
- Enviar los datos procesados a Elasticsearch para su almacenamiento y análisis.

**Configuración clave:**
- Los logs estructurados se procesan con un parser JSON nativo.
- Los logs clásicos se procesan mediante expresiones regulares para extraer campos como `timestamp`, `level` y `message`.

**Documentación oficial de Fluent Bit:**
- [Introducción a Fluent Bit](https://docs.fluentbit.io/manual)
- [Configuración de pipelines](https://docs.fluentbit.io/manual/concepts/data-pipeline)
- [Parsers en Fluent Bit](https://docs.fluentbit.io/manual/pipeline/parsers)

### 🗄️ Elasticsearch

**Elasticsearch** es un motor de búsqueda y análisis distribuido que actúa como el núcleo del almacenamiento en **Analog**. Los logs procesados por Fluent Bit se almacenan en índices de Elasticsearch para permitir:

- Consultas rápidas utilizando la sintaxis de búsqueda de **Lucene**.
- Creación de visualizaciones en **Grafana** (o **Kibana** si se quiere!).

**Configuración clave:**

- **Arquitectura de nodos**:
  - 1 nodo maestro: Administra el clúster y las tareas de coordinación.
  - 2 nodos de datos: Manejan el almacenamiento y procesamiento de datos.
- **Sin autenticación ni TLS**: Elasticsearch esta configurado para un entorno de laboratorio, lo que simplifica la implementación inicial al deshabilitar la seguridad.
  - Esto incluye `xpack.security.enabled=false` en la configuración para deshabilitar la autenticación.
- **Índices personalizados**:
  - `app_structured_logs`: Logs estructurados en formato JSON.
  - `app_classic_logs`: Logs clásicos extraídos con expresiones regulares.
- **Mappings**: Cada índice cuenta con propiedades específicas:
  - `timestamp`: Tipo `date`.
  - `lvl`: Tipo `keyword`.
  - `message`: Tipo `text`.

**Nota importantes! 🔊**

- **Los datos no persisten por diseño**. Esto es intencional, ya que el objetivo del proyecto es ofrecer un entorno de pruebas y aprendizaje donde los datos sean desechables. Esto facilita iteraciones rápidas sin preocuparse por la acumulación de logs históricos o la gestión de almacenamiento.
- En caso de querer persistir datos de ElasticSearch, se pueden montar volumenes mapeando `/usr/share/elasticsearch/data`.
- Ojo si se decide utilizar este clúster en una PC con poco rendimiento. El arranque de los servicios puede ser muy demandante por un breve periodo de tiempo.
- Aca esta incluido Kibana. Usualmente van de la mano y es muy util.

**Documentación oficial de Elasticsearch:**
- [Introducción a Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [API REST de Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)
- [Estructuración de datos: mappings](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)
- [Que es Kibana?](https://www.elastic.co/guide/en/kibana/current/introduction.html)

### 📊 Grafana

Aunque Grafana no es parte directa del procesamiento de logs, actúa como el componente visual de la infraestructura.

---

## 🚀 Despliegue

### 1. Crear la red compartida

Antes de iniciar los servicios, asegurate de contar con la red compartida necesaria para la comunicación entre contenedores:

```bash
docker network create analog_network
```

### 2. Levantar los servicios

Ejecuta los siguientes comandos para iniciar los servicios por separado:

```bash
docker-compose -f docker-compose-structured.yml up --build -d
docker-compose -f docker-compose-classic.yml up --build -d
docker-compose -f docker-compose-elasticsearch.yml up --build -d
docker-compose -f docker-compose-grafana.yml up --build -d
```

---

## 🔄 Administración de contenedores

### Reiniciar un archivo específico:

```bash
docker-compose -f <archivo-docker-compose>.yml down
docker-compose -f <archivo-docker-compose>.yml up --build
```

### Reiniciar un contenedor específico:

```bash
docker restart <nombre-contenedor>
```

### Reiniciar todos los servicios:

```bash
docker-compose -f docker-compose-structured.yml down
docker-compose -f docker-compose-classic.yml down
docker-compose -f docker-compose-elasticsearch.yml down
docker-compose -f docker-compose-grafana.yml down

docker-compose -f docker-compose-structured.yml up --build -d
docker-compose -f docker-compose-classic.yml up --build -d
docker-compose -f docker-compose-elasticsearch.yml up --build -d
docker-compose -f docker-compose-grafana.yml up --build -d
```

### Apagar todos los servicios sin eliminar volúmenes:

```bash
docker-compose -f docker-compose-structured.yml down
docker-compose -f docker-compose-classic.yml down
docker-compose -f docker-compose-elasticsearch.yml down
docker-compose -f docker-compose-grafana.yml down
```

### Eliminar todos los contenedores y red:

```bash
docker-compose -f docker-compose-structured.yml down
docker-compose -f docker-compose-classic.yml down -v
docker-compose -f docker-compose-elasticsearch.yml down
docker-compose -f docker-compose-grafana.yml down

docker network rm analog_network
```

---

## 📖 Notas Adicionales

### Ver contenedores activos:

```bash
docker ps
```

### Inyectar datos manualmente en Elasticsearch:

```bash
curl -XPOST 'http://elasticsearch_master:9200/_bulk' -H 'Content-Type: application/json' -d '
{ "index" : { "_index" : "app_structured_logs" } }
{ "timestamp": "2025-01-08T19:36:00Z", "lvl": "INFO", "message": "Test message from Fluent-bit" }
{ "index" : { "_index" : "app_structured_logs" } }
{ "timestamp": "2025-01-08T19:36:01Z", "lvl": "WARN", "message": "Another test message from Fluent-bit" }
'
```

### Crear un índice en Elasticsearch:

```bash
curl -XPUT http://elasticsearch_master:9200/app_structured_logs -H 'Content-Type: application/json' -d '{
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "lvl": { "type": "keyword" },
      "message": { "type": "text" }
    }
  }
}'
```

### Ver información útil en Elasticsearch:

- Buscar logs en un índice: [http://localhost:9200/app_structured_logs/_search?pretty](http://localhost:9200/app_structured_logs/_search?pretty)
- Ver índices disponibles: [http://localhost:9200/_cat/indices?v](http://localhost:9200/_cat/indices?v)
- Página principal de Elasticsearch: [http://localhost:9200/](http://localhost:9200/)
- Dashboard de Grafana: [http://localhost:3000/dashboards](http://localhost:3000/dashboards)

### Ejecutar un dummy manualmente:

```bash
/opt/fluent-bit/bin/fluent-bit -i dummy -o es://elasticsearch_master:9200 \
  -p Index=app_structured_logs \
  -p Logstash_Format=Off \
  -p Suppress_Type_Name=On \
  -p Replace_Dots=On \
  -f 1
```

---

## 📊 Dashboards Preconfigurados

Grafana incluye dashboards preconfigurados para visualizar los logs recolectados en formato estructurado y clásico. Estos dashboards permiten:

- Analizar niveles de log (INFO, WARN, ERROR).
- Contar logs por mensaje.
- Ver eventos en tiempo real.

**Acceso a Grafana:** [localhost](http://localhost:3000)  
**Usuario por defecto:** `TraeteTuUsuario`  
**Contraseña:** `yContraseña!`

---

## 🧩 Persistencia de Datos

Para evitar configurar manualmente el dashboard en cada reinicio, Grafana persiste los datos en el directorio `grafana_data`.