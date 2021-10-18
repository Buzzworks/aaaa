#!/bin/sh
##
##  new-server-cert.sh - create the server cert
##  Copyright (c) 2000 Yeak Nai Siew, All Rights Reserved. 
##
blink='\e[5m'
g='\e[38;5;82m'
r='\e[1;31;47m'
c='\e[0m'

# Create the key. This should be done once per cert.
CERT=$1
if [ $# -ne 1 ]; then
        echo -e "$r Usage: $0 <www.domain.com>$c"
        echo ""
        exit 1
fi
if [ ! -f $CERT.key ]; then
	echo -e "$r No $CERT.key round. Generating one$c"
	echo ""
	openssl genrsa -out $CERT.key 4096
	echo ""
fi

# Fill the necessary certificate data
CONFIG="server-cert.conf"
cat >$CONFIG <<EOT
[ req ]
default_bits			= 4096
default_keyfile			= server.key
distinguished_name		= req_distinguished_name
string_mask			= nombstr
req_extensions			= v3_req
[ req_distinguished_name ]
countryName			= Country Name (2 letter code)
countryName_default		= MY
countryName_min			= 2
countryName_max			= 2
stateOrProvinceName		= State or Province Name (full name)
stateOrProvinceName_default	= Perak
localityName			= Locality Name (eg, city)
localityName_default		= Sitiawan
0.organizationName		= Organization Name (eg, company)
0.organizationName_default	= My Directory Sdn Bhd
organizationalUnitName		= Organizational Unit Name (eg, section)
organizationalUnitName_default	= Secure Web Server
commonName			= Common Name (eg, www.domain.com)
commonName_max			= 64
emailAddress			= Email Address
emailAddress_max		= 40
[ v3_req ]
nsCertType			= server
keyUsage 			= digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
basicConstraints		= CA:false
subjectKeyIdentifier		= hash
EOT

echo -e "$g Fill in certificate data$c"
openssl req -new -config $CONFIG -key $CERT.key -out $CERT.csr

rm -f $CONFIG

echo ""
echo -e "$g You may now run $r./sign-server-cert.sh $CERT $c to get it signed$c"
