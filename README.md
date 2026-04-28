# TankYou

## 🇪🇸 Descripción

TankYou es una aplicación web de **recarga telemática de combustible**, desarrollada como proyecto final de DAW.

La plataforma permite a los clientes gestionar todo el proceso de forma online:

- Registro e inicio de sesión de usuarios
- Alta y gestión de vehículos
- Reserva de recargas seleccionando **día y hora**
- Sistema de agenda con **máximo de recargas por franja horaria**
- Selección automática de la franja disponible más conveniente
- Gestión de pedidos y recargas desde panel interno

La aplicación está pensada para digitalizar y optimizar el proceso de repostaje programado.

## 🚀 Demo en vivo

https://tankyouapp.online/

## 🛠 Tecnologías utilizadas

- Django
- PostgreSQL
- Docker
- Docker Compose
- Docker Swarm
- Nginx
- HTML / CSS / JavaScript

## ⚙️ Infraestructura

- Despliegue en servidor real
- Separación de entorno desarrollo / producción
- Contenedorización completa con Docker
- Proxy inverso con Nginx

## 💻 Ejecución local

> La configuración de producción pertenece a un servidor privado y no está incluida en este repositorio.

Para ejecutar el proyecto en local solo necesitas:

- Docker
- Docker Compose

### Pasos

```bash
docker compose up --build