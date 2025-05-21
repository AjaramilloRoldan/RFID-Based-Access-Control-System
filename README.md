
# RFID-Based Access Control System

Sistema de control de acceso basado en tecnología RFID que utiliza un módulo ESP8266 y un backend desarrollado con Flask para automatizar el registro y monitoreo de accesos en entornos institucionales.

---

## Descripción

Este proyecto automatiza el control de acceso tradicional, reemplazando los registros manuales por un sistema electrónico que permite la lectura de tarjetas RFID para validar y registrar entradas y salidas. La solución ofrece monitoreo en tiempo real y herramientas administrativas para gestionar accesos, aumentando la seguridad y eficiencia.

El sistema redujo el acceso no autorizado en un 75% y es capaz de manejar más de 1,000 registros mensuales con buena performance.

---

## Tecnologías utilizadas

- Python
- Flask
- MySQL
- HTML5, CSS3, Bootstrap
- RFID
- ESP8266 (microcontrolador con WiFi)

---

## Características principales

- Lectura y validación de tarjetas RFID para autorizar accesos.
- Registro automático y almacenamiento de logs en base de datos MySQL.
- Panel web administrativo para visualización y gestión de usuarios y accesos.
- Monitorización en tiempo real de accesos.
- Sistema optimizado para manejo eficiente de más de 1,000 registros mensuales.
- Control basado en roles para diferentes niveles de usuario.

---

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

2. Crea un entorno virtual e instala las dependencias:

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configura la base de datos MySQL con las tablas necesarias (ver scripts en `/database`).

4. Configura las credenciales y parámetros en el archivo de configuración (`config.py` o similar).

5. Corre el servidor Flask:

```bash
flask run
```

6. Configura el ESP8266 con el código y ajusta la conexión al servidor Flask.

---

## Uso

- Accede al panel web para agregar usuarios y gestionar accesos.
- Utiliza tarjetas RFID para ingresar y registrar accesos automáticamente.
- Revisa los logs de acceso en tiempo real desde el panel administrativo.
- Administra permisos y control de usuarios según roles.

---


## Contribuciones

Si deseas contribuir al proyecto, por favor abre un issue o envía un pull request. Toda ayuda es bienvenida.

---

## Contacto

Alejandro Jaramillo  
Correo: jaramilloalejandro790@gmail.com  
LinkedIn: [https://www.linkedin.com/in/ajaramilloroldan/](https://www.linkedin.com/in/ajaramilloroldan/)

---

## Licencia

Este proyecto está bajo la licencia MIT - consulta el archivo LICENSE para más detalles.

```
