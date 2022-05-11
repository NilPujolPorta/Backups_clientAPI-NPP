# Config guide

### **Read this in other languages: [English](README.md), [Español](README.ES-es.md), [Català](README.CA-ca.md).**

## Structure

-BD:

***database***: \<Database Name>

***host***: \<Host>

***passwd***: \<Password>

***user***: \<Username>

## Usage

- Do not chane anything apart from the values marked with <>
- The Host must be without port, only ip. It only works with the default port.
- Spaces can cause problems. If used use  ""

### Examples

    - BD:
        database: backups
        host: 172.23.121.6
        passwd: potato
        user: backupsUser

    - BD:
        database: "backups database"
        host: myMySQLServer.mydomain.com
        passwd: idk.createP4sswd()
        user: "Jhon Smith"