# Tuto Simple Postfix architecture


## Objectif

Monter une infra simple afin de faciliter la compréhension des protocoles de messagerie.
L'infra se veut souple pour pouvoir progressivement permettre de se complexifier.


## Mise sur pied initiale

##### L'architecture de base est la suivante:
- Alice: 1 VM sous Debian 11, avec MUA 
- Bob: 1 VM sous Debian 11, avec MUA, MSA différent de Alice
- Charlie: Optionnel, 1 VM sous Debian 11, avec MUA, MSA de Alice
- MTA1: 1 VM sous Debian 11, avec serveur Postfix, MSA de A et MDA pour Bob 
- MTA2: 1 VM sous Debian 11, avec serveur Postfix, MSA de A et MDA pour Bob 

##### Réseaux mis en place:

Domaine | Machines | Réseau + masque | Remarques 
 --- | --- | --- | ---
 A | MTA1, Alice, Charlie | 192.168.1.0/24 | 
 B | MTA2, Bob | 192.168.2.0/24 | 
 1 | MTA1, MTA2 | 10.0.0.0/30 | Simulation Internet 


## Protocole d'installation

### Montage des serveurs Postfix

#### Installation

##### Base des VMs

- Créer une machine Debian minimale.

> Exemple de conf machine: RAM 1024Mo, 1 processeur, 64MB de mem graphique

- La dupliquer pour avoir les bases des 2 types de machines:
    - Base des serveurs PostFix (MTA)
    - Base des machines utilisateurs (MUA)


##### Base des MTA

Sur le clone réalisé:

- Ajouter une interface réseau (en plus de l'interface NAT par défaut):
1. L'interface NAT (enp0s3) servira ensuite pour le domaine interne (domaine A ou B).
2. L'interface supplémentaire (enp0s8) sert pour la liaison entre les MTA (domaine 1). Il faut la configurer en mode réseau interne.

- Installer les paquets postfix, dovecot et les utilitaires réseau.
```bash
sudo apt-get install postfix dovecot-imapd tcpdump mailutils telnet
```
> *Postfix* est un MTA libre, pendant l'install, préciser `systeme satellite`, le restant par défaut (sera reconfiguré après).
> *dovecot* est un utilitaire qui permet de fournir des démons pour les serveurs IMAP et POP3 pour Postfix. On utilisera IMAP.
> *tcpdump* permet d'écouter
> *mailutils* contient les commandes basiques d'envoi de mail

##### Base des MUA

Sur l'image initiale:

- Créer une Debian minimale avec environnement graphique (Xfce > moins gourmand) avec un compte alice et une autre avec un compte Bob

- Configurer l'interface réseau sur les domaines internes respectifs A et B

- Installer le paquet Thunderbird
```bash
sudo apt-get install thunderbird
```
> Installer les additions invité, ça fait gagner du temps...

> Si un utilisateur n'est pas Sudoer, ajouter au groupe *sudo*:
> ```bash
> su
> sudo usermod -aG sudo <user>
> sudo reboot
> ```

#### Configuration des MTA

##### Interfaces

Pour simplifier le fonctionnement, pas de DHCP sur les liaisons dans un premier temps (conf `static`). Il est également nécessaire d'activer le routage (possible sous debian mais désactivé par défaut...)

- Editer la conf network (`/etc/network/interfaces`) et y ajouter la conf statique pour le *domaine 1*:
```
# Link with users
auto enp0s3
iface enp0s3 inet static
    address 192.168.1.1/24

# Link with orher Postfix
auto enp0s8
iface enp0s8 inet static
    address 10.0.0.1/30
    up ip route add 192.168.2.0/24 via 10.0.0.2
```
> NB: La dernière ligne permet d'introduire une règle de routage statique

- Activer le routage en éditant le fichier `/etc/sysctl.conf`, en dé-commentant la ligne `net.ipv4.ip_forward=1`.

- Cloner la VM pour avoir les deux MTA, modifier la conf network (`/etc/network/interfaces`) du deuxième MTA au niveau des l'adresses réseau:
 - adresse enp0s3: 192.168 **.2** .1 au lieu de 192.168 **.1** .1
 - adresse enp0s8: 10.0.0 **.2** au lieu de 10.0.0 **.1**
 - routage destination: 192.168 **.1** .0 au lieu de 192.168 **.2**.0
 - routage relais: 10.0.0 **.1** au lieu de 10.0.0 **.2**.

> Sur les deux machines, relancer le réseau avec la commande:
> ```bash
> sudo systemctl restart networking
> ```

- Tester la connexion entre les MTA.
> Sur une machine, lancer l'écoute avec *tcpdump*:
> ```bash
> sudo tcpdump -i enp0s8 icmp
> ```
> Sur l'autre, initier des pings:
> ```bash
> ping 10.0.0.1
> ```

> NB: pour les curieux, pour voir la table de routage, exécuter `ip route show`


##### Résolution de noms

En local (plus simple qu'installer un serveur DNS), on modifie `/etc/hosts`, en ajoutant les lignes:
```
# Résolutions locales
10.0.0.1    mta1.loc
10.0.0.2    mta2.loc
```

> **NB:** Sous linux, le fichier `hosts` est accédé avant le DNS précisé dans `resolv.conf`...
> On peut ainsi shunter la résolution DNS, ou la configurer sur un autre DNS avec un `nameserver`.

> Pour installer un DNS simple sous linux, `bind9`.


##### Postfix

Ajouter l'utilisateur comme *Postmaster*, en éditant (en *root*) le fichier `/etc/aliases`
```
postmaster: root # Relaie les messages d'administration mail vers le compte root
root: debian # Relaie les messages du root vers l'utilisateur debian
```

> Ceci permet de fusionner les boites *postmaster*, *root* et *debian* dans la mailbox de *debian*.
Pour prendre en compte les changements:
```bash
sudo newaliases
```

Reconfiguration Postfix, en éditant le fichier de conf `/etc/postfix/main.cf`

Pour MTA1:
```
myhostname = mta1.loc
relayhost = [10.0.0.2]
mynetworks = ... 10.0.0.0/30 192.168.1.0/24
inet_interfaces = all
```
Puis on relance le service Postfix avec: 
```bash
sudo systemctl restart postfix
```

Pour MTA2:
```
myhostname = mta2.loc
relayhost = [10.0.0.1]
mynetworks = ... 10.0.0.0/30 192.168.2.0/24
inet_interfaces = all
```

> **NB:** Pour shunter la résolution DNS du MX, il est nécessaire pour nous de mettre le serveur relai entre crochets...
> Il est impératif dans le cas d'une résolution DNS d'ajouter sur le serveur de noms une ligne MX 

##### Test

Sur le MTA1 (Chaque retour à la ligne correspond à une pression sur entrée, avec une réponse en 200 ou 300 du serveur) :
```
telnet 10.0.0.2 25
mail from: toto
rcpt to:postmaster@mta2.loc
data
Subject: Objet du mail
Ici on met le corps du mail.
.
quit
```

##### Ajouter des utilisateurs sur un Postfix
La manière la plus simple consiste à ajouter un utilisateur sur le Debian.
Par exemple, pour ajouter une boite e-mail à charlie (`charlie@mta1.loc`), aller sur le MTA1, puis créer un utilisateur et enregistrer son MdP:
```bash
sudo useradd charlie
sudo passwd charlie
```
Et c'est tout! `:)`


#### Configuration des MUA

##### Interfaces

Pour simplifier le fonctionnement, pas de DHCP sur les liaisons dans un premier temps (conf `static`).

*1. Alice*
- Editer la conf network (`/etc/network/interfaces`) de Alice et y ajouter la conf statique pour le *domaine 1*:
```
# Link with Postfix server
auto enp0s3
iface enp0s3 inet static
    address 192.168.1.2/24
    gateway 192.168.1.1
```

- Résolutions DNS en local `sudo nano /etc/hosts`, en ajoutant les lignes:
```bash
# Résolutions locales
10.0.0.1    mta1.loc
10.0.0.2    mta2.loc
```

- Relancer le service:  
```bash 
sudo systemctl restart networking
```

- Tester la connexion avec le MTA.
Sur le MTA, lancer l'écoute avec tcp dump:
```bash
sudo tcpdump -i enp0s3 icmp
```
Sur Alice, initier des pings:
```bash
ping 192.168.1.1
```

*2. Bob*
- Editer la conf network (`/etc/network/interfaces`) de Alice et y ajouter la conf statique pour le *domaine 2*:

```
# Link with Postfix server
auto enp0s3
iface enp0s3 inet static
    address 192.168.2.2/24
    gateway 192.168.2.1
```

- Résolutions DNS en local `sudo nano /etc/hosts`, en ajoutant les lignes:
```bash
# Résolutions locales
10.0.0.1    mta1.loc
10.0.0.2    mta2.loc
```

- Relancer le service:  
```bash
sudo systemctl restart networking
```

- Tester la connexion avec le MTA.
Sur le MTA, lancer l'écoute avec tcp dump:
```bash
sudo tcpdump -i enp0s3 icmp
```
Sur l'autre, initier des pings:
```bash
ping 192.168.2.1
```

##### Ajout des certificats S/MIME

Génerer des certificats avec une AC auto-signée, puis générer les certificats de Alice et de Bob.
> **Important:** Certificats
> 
> *Root CA configuration:* Export PEM
> - nsComment=xca certificate
> - nsCertType=sslCA, emailCA, objCA
> - keyUsage=critical,keyCertSign, cRLSign
> - subjectKeyIdentifier=hash
> - basicConstraints=critical,CA:TRUE
> 
> *Alice cert conf:* Export #PKCS12 pour Alice et PEM pour Bob
> - nsComment=xca certificate
> - nsCertType=client, email
> - subjectAltName=DNS:alice@mta1.loc, email:alice@mta1.loc
> - extendedKeyUsage=clienAuth, emailProtection
> - keyUsage=digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment, keyAgreement
> - subjectKeyIdentifier=hash
> - basicConstraints=critical,CA:FALSE
> 
> *Bob cert conf:* Export #PKCS12 pour Bob et PEM pour Alice
> - nsComment=xca certificate
> - nsCertType=client, email
> - subjectAltName=DNS:bob@mta2.loc, email:bob@mta2.loc
> - extendedKeyUsage=clientAuth, emailProtection
> - keyUsage=digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment, keyAgreement
> - subjectKeyIdentifier=hash
> - basicConstraints=critical,CA:FALSE


Pour les ajouter sur les Thunderbird:
1. Menu (Les 3 barres...) > `Account Settings` > Onglet `End-To-End Encryption`
2. § `S/MIME`, cliquer sur `Manage S/MIME Certificates`
   1. Dans l'onglet `Your Certificates`, cliquer sur `Import...` puis sélectionner le fichier P12 de l'utilisateur concerné (et mettre le MdP correspondant).
   2. Dans l'onglet `People`, `Import...`, ajouter les CRT des autres utilisateurs.
   3. Dans l'onglet `Authorities`, `Import...`, ajouter le CRT du *Root CA*, puis cliquer sur `OK` (*NB:*Il existe sans doute déja, importé avec le P12)
   4. !!! Onglet `Authorities`, sélectionner le certificat du *Root CA*, `Edit trust...`, cocher `This certificate can identify mail users` !!!
3. De retour dans le § `S/MIME`, item `Personal certificate for digital signing`, `Select...`, sélectionner l'utilisateur (*NB:*il ne doit y en avoir qu'un logiquement...)
4. Une pop-up vous propose de prendre le même certificat pour le chiffrement, dans le cas contraire même manip avec l'item `Personal certificate for encryption`.
5. Il est possible de choisir de signer par défaut ses messages, ou de les chiffrer.

> **NB:** Ajout d'un répertoire partagé sous VBox:
> 1. Ajouter les additions invités
> 2. Ne pas oublier le sudo `useradd -aG vboxsf <user>`
> 3. Puis `sudo reboot`




##### Installation extension TDB

> ToDo
