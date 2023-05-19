# Gymnastique avec OpenSSL, S/MIME, TELNET, CERTUTIL 

## Jouer avec les certificats

### Chemin par défaut des certificats sous Linux (accédés par OpenSSL):
```bash
openssl version -d
```

Parmi les sous-répertoires:
- `certs`: contient les certificats publics
- `private`: contient les clés privées

### Extraction de la clé privée d'un p12:
```bash
openssl pkcs12 -in certificate.p12 -out privkey.pem
```
- Le premier MdP est celui du PKCS12;
- La passphrase suivante est le MdP de protection de la clé privée;


## Avec un message test.msg

### Extraire le contenu d'un message:
> Uniquement message déchiffré

- noverify pour shunter la vérification de signature

```bash
openssl smime -verify -noverify -text -in test.msg
```

> Répond `Verification successful` mais n'a rien vérifié...


### Tester la signature (sortie STDOUT) et enregistrer le message:
> idem: uniquement message de type `pkcs7-signature`

- CAfile: précise la CA des signatures (obligatoire)

```bash
openssl smime -verify -CAfile ./CERTS/Root_CA.crt -in test.msg -out plain_text.txt
```
> Pour ne pas enregistrer, déviser la sortie avec `-out /dev/null`


## Jouer avec certutil














## Avec un message test_crypted.msg

### Dechiffrement avec clé privée:
```bash
openssl smime -decrypt -in test_crypted.msg -recip BobPriv.pem -out test_decrypted.msg
```
> Nécessaire si signé+ chiffré

### Rechiffrement avec clé publique
```bash
openssl smime -encrypt -in test_decrypted.msg -recip Charlie.crt -out test_recrypted.msg
```
> Nécessaire si signé+ chiffré

## Telnet SMTP message

### Envoi de message via telnet

- Ouvrir une session telnet sur le bon MTA
```bash
telnet mta2.loc 25
```

- Ouvrir une session SMTP
```bash
EHLO mta2.loc
```

- Envoi du message
```bash
MAIL FROM: alice@mta1.loc
RCPT TO: charlie@mta1.loc
DATA
X-forwarded-by: bob@mta2.loc
<contenu du message>
.
```

