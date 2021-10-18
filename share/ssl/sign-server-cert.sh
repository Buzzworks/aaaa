#!/bin/sh
##
##  sign-server-cert.sh - sign using our root CA the server cert
##  Copyright (c) 2000 Yeak Nai Siew, All Rights Reserved. 
##
blink='\e[5m'
g='\e[38;5;82m'
r='\e[1;31;47m'
c='\e[0m'

SERIAL=`date +"%d"`
CERT=$1
if [ $# -ne 1 ]; then
        echo -e "$r Usage: $0 <www.domain.com>$c"
        exit 1
fi
if [ ! -f $CERT.csr ]; then
        echo -e "$r No $CERT.csr round. You must create that first.$c"
	exit 1
fi
# Check for root CA key
if [ ! -f ca.key -o ! -f ca.crt ]; then
	echo -e "$r You must have root CA key generated first.$c"
	exit 1
fi

# Sign it with our CA key #

#   make sure environment exists

if [ ! -d ca.db.certs ]; then
    mkdir ca.db.certs
fi

if [ ! -f ca.db.$SERIAL.serial ]; then
    echo "$SERIAL" >ca.db.$SERIAL.serial
fi

if [ ! -f ca.db.index ]; then
    cp /dev/null ca.db.index
fi

#  create the CA requirement to sign the cert
cat >ca.config <<EOT
[ ca ]
default_ca              = default_CA
[ default_CA ]
dir                     = .
certs                   = \$dir
new_certs_dir           = \$dir/ca.db.certs
database                = \$dir/ca.db.index
serial                  = \$dir/ca.db.$SERIAL.serial
certificate             = \$dir/ca.crt
private_key             = \$dir/ca.key
default_days            = 1825
default_crl_days        = 30
default_md              = sha256
preserve                = no
x509_extensions		= server_cert
policy                  = policy_anything
[ policy_anything ]
countryName             = optional
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional
[ server_cert ]
basicConstraints	= CA:FALSE
subjectKeyIdentifier 	= hash
authorityKeyIdentifier	= keyid,issuer
keyUsage 		= digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName		= @subject_alt_names

[ subject_alt_names ]
DNS.1 			= *.google.com
IP.1			= $CERT
IP.2			= 127.0.0.1
IP.3			= ::1	
EOT

#  sign the certificate
echo -e "$g CA signing: $CERT.csr -> $CERT.crt: $c"
openssl ca -config ca.config -out $CERT.crt -infiles $CERT.csr
echo -e "$g CA verifying: $CERT.crt <-> CA cert $c"
openssl verify -CAfile ca.crt $CERT.crt

#  cleanup after SSLeay 
rm -f ca.config
rm -f ca.db.serial.old
rm -f ca.db.index.old

echo -e "$g You Have Successfully Generated Server Certificates For Your Server$c"
echo ""
echo -e "Certificate file               =$g $CERT.crt $c"
echo -e "Certificate Key file           =$g $CERT.key $c"
echo -e "Certificate Sign Request file  =$g $CERT.csr $c"
echo ""
