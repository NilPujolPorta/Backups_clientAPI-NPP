# Guia de configuració

### **Llegeix en altres idiomes: [English](README.md), [Español](README.ES-es.md), [Català](README.CA-ca.md).**

## Estructura

-BD:

***database***: \<Nom de la base de dades>

***host***: \<Amfitrió>

***passwd***: \<Contrassenya>

***user***: \<Nom d'usuari>

## Ús

- No canviar res apart dels valors entre <>
- El amfitrió no ha de tenir port, només ip. La base de dades ha de estar en el port per defecte.
- Els espais poden causar problemes. Si s'utilitzen usar:  ""

### Exemples

    - BD:
        database: backups
        host: 172.23.121.6
        passwd: patata
        user: UsuariBackups

    - BD:
        database: "Copies de seguretat"
        host: elMeuMySQLServer.elMeuDomini.com
        passwd: ns.crearContr4assenya()
        user: "Jordi Pujol"