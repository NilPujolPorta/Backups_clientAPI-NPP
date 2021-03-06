# Error logs guide

### **Read this in other languages: [English](README.md), [Español](README.ES-es.md), [Català](README.CA-ca.md).**

## File structure:
``date``--``hour``-``errorType``.txt

## Active backup specific error codes:
```
100 Unknown error
101 No parameter of API, method or version
102 The requested API does not exist
103 The requested method does not exist
104 The requested version does not support the functionality
105 The logged in session does not have permission
106 Session timeout
107 Session interrupted by duplicate login
119 SID not found
400 Invalid parameter of file operation
401 Unknown error of file operation
402 System is too busy
403 Invalid user does this file operation
404 Invalid group does this file operation
405 Invalid user and group does this file operation
406 Can't get user/group information from the account server
407 Operation not permitted
408 No such file or directory
409 Non-supported file system
410 Failed to connect internet-based file system (e.g., CIFS)
411 Read-only file system
412 Filename too long in the non-encrypted file system
413 Filename too long in the encrypted file system
414 File already exists
415 Disk quota exceeded
416 No space left on device
417 Input/output error
418 Illegal name or path
419 Illegal file name
420 Illegal file name on FAT file system
421 Device or resource busy
599 No such task of the file operation
```