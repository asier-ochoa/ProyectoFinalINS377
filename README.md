# Proyecto final para Bases de Datos I

- **Integrantes**:
    - Asier Ochoa 1101331
    - David Quezada 1066865
    - Abraham Abreu 1099026
    - (nombre)

## Como instalar:
### Requerimientos:
- Python 3.10
- pip
- MariaDB C connector [enlace](https://mariadb.com/downloads/connectors/)

Asegurarse tener pipenv instalado:
```
pip install pipenv
```

Clonar repositorio y activar entorno:
```
git clone https://github.com/asier-ochoa/ProyectoFinalINS377
cd ProyectoFinalINS377
pipenv install
```

## Diseño de la base de datos:

Las entidades centrales son los proveedores de anuncios (personas que quieren 
anunciar un producto) y los receptores de anuncios (dueños de sitios web que 
proveen espacio para anuncios). 

Se necesitan trazar los siguientes casos:
- Anuncios en circulacion por proveedor
- Anuncios sometidos por categoria de interes
- Lista de campañas de anuncios contratadas
- Traza de visualizaciones
- Ordenacion de sitios web por trafico
- Ordenacion de campañas de anuncio por mas mostrados
- (mas casos todavia no considerados)
