# Guia de configuración

### **Lee en Otros idiomas: [English](README.md), [Español](README.ES-es.md), [Català](README.CA-ca.md).**

## Estructura

-BD:

***database***: \<Nombre de la base de datos>

***host***: \<Anfitrión>

***passwd***: \<Contrasseña>

***user***: \<Nombre de usuario>

## Uso

- No canviar nada aparte de los valores entre <>
- El anfitrión no hay que especificar puerto, solo ip. La base de datos tiene que estar en el puerto defecto.
- Los espacios pueden causar problemas. Si se usan tambien usar:  ""

### Ejemplos

    - BD:
        database: backups
        host: 172.23.121.6
        passwd: patata
        user: UsuarioBackups

    - BD:
        database: "Copias de seguridad"
        host: miMySQLServer.midomini.com
        passwd: ns.crearContr4asseña()
        user: "Juan Rodriguez"