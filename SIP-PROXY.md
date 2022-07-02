# SIP Proxy Setup - Kamailio


Where in this setup we would consider the below-mentioned components.

* Single Kamailio Server
* Single RTPEngine Server
* Two FreeSWITCH Server

## RTPEngine

### Installation

Installation can normally be carried out through source code from git repository.
However, for quicker and easier installation binary installation from a repository is easy where we have to build those binary and available on our
repository as well.

#### Debian 11:
```
echo 'deb http://download.opensuse.org/repositories/home:/ganapathi/Debian_11/ /' | sudo tee /etc/apt/sources.list.d/home:ganapathi.list
curl -fsSL https://download.opensuse.org/repositories/home:ganapathi/Debian_11/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_ganapathi.gpg > /dev/null
sudo apt update
sudo apt install rtpengine
```

#### Ubuntu 20.04:
```
echo 'deb http://download.opensuse.org/repositories/home:/ganapathi/xUbuntu_20.04/ /' | sudo tee /etc/apt/sources.list.d/home:ganapathi.list
curl -fsSL https://download.opensuse.org/repositories/home:ganapathi/xUbuntu_20.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_ganapathi.gpg > /dev/null
sudo apt update
sudo apt install rtpengine
```

#### Redhat-8:

```
cat <<EOT > /etc/yum.repos.d/flexydial.repo
[Flexydial_Repo]
name=Flexydial Repo - RHEL-\$releasever-\$basearch
baseurl=http://flexy-repo.s3-website-us-east-1.amazonaws.com/rhel/\$releasever/\$basearch
enabled=1
gpgkey=http://flexy-repo.s3-website-us-east-1.amazonaws.com/RPM-GPG-KEY-ganapathi
gpgcheck=1
EOT

sudo dnf update
sudo dnf install ngcp-rtpengine
```

### Configuration

1. Open /etc/rtpengine/rtpengine.conf and edit **interface** option and **listen-ng** accordingly mentioned below.

      From:
      ```
      interface = any
      ```
      To:
      ```
      interface = REPLACE_PRIVATE_IP!REPLACE_PUBLIC_IP
      ```

Note: Replace with your actual private and public IP address in that interface option.

2. Replace **listen-ng** to listen on all ipv4 addresses on the server by editing **/etc/rtpengine/rtpengine.conf** as mentioned below.

      From:
      ```
      listen-ng = localhost:2223
      ```
      To:
      ```
      listen-ng = 0.0.0.0:2222
      ```
3. Start rtpengine service and enable it once for system startup.

      ```
      systemctl enable rtpengine
      systemctl start rtpengine
      ```

## Kamailio

### Installation:

#### Debian 11:
```
wget -O- https://deb.kamailio.org/kamailiodebkey.gpg | sudo apt-key add -
tee /etc/apt/sources.list.d/kamailio.list<<EOF
deb     http://deb.kamailio.org/kamailio55 bullseye main
deb-src http://deb.kamailio.org/kamailio55 bullseye main
EOF
sudo apt update
sudo apt install kamailio kamailio-mysql-modules kamailio-websocket-modules kamailio-tls-modules kamailio-postgres-modules kamailio-presence-modules
```

#### Ubuntu 20.04:
```
wget -O- https://deb.kamailio.org/kamailiodebkey.gpg | sudo apt-key add -
tee /etc/apt/sources.list.d/kamailio.list<<EOF
deb     http://deb.kamailio.org/kamailio55 focal main
deb-src http://deb.kamailio.org/kamailio55 focal main
EOF
sudo apt update
sudo apt install  kamailio kamailio-mysql-modules kamailio-websocket-modules kamailio-tls-modules kamailio-postgres-modules kamailio-presence-modules
```

#### Redhat-8:

```
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://rpm.kamailio.org/centos/kamailio.repo
sudo dnf install kamailio kamailio-mysql-modules kamailio-websocket-modules kamailio-tls-modules kamailio-postgres-modules kamailio-presence-modules
```


### Configuration:

1. Replace below mentioned variable value as per our configuration.

      /etc/kamailio/kamctlrc:

      ```
      DBENGINE=MYSQL
      DBHOST=localhost
      SIP_DOMAIN=ks.flexydial.com
      ```
2. Create Kamailio mysql table which is necessary for Kamailio setup.

      ```
      kamdbctl create
      ```

3. Create Self-Signed SSL or place valid SSL certificate, keys files into **/etc/kamailio** folder and make sure necessary file permission and do replace certificate and key filename on tls.cfg under this Kamailio configuration.

    /etc/kamailio/tls.cfg
    ```
    [server:default]
    method = TLSv1.2+
    verify_certificate = no
    require_certificate = no
    private_key = privkey.pem
    certificate = fullchain.pem
    ```

4. Replace below mentioned configuration on **/etc/kamailio/kamailio-local.cfg** and keep the other configuration as it is.

    ```
    #!substdef "/MY_PUBLIC_IP/3.80.131.170/"
    #!substdef "/MY_PRIVAYE_IP/10.164.29.126/"
    #!substdef "/SIP_PORT/5060/"
    #!substdef "/WSS_PORT/7443/"

    #!substdef "/MY_FS_PORT/45060/"

    #!define PG_DBURL       "postgres://postgres:password@127.0.0.1:5432/flexydial"
    #!define MY_DBURL       "mysql://kamailio:kamailiorw@localhost/kamailio"
    #!define RTPENGINE_SOCK "udp:127.0.0.1:2222"
    alias="ks1.flexydial.com"
    ```
5. Copy below mentioned configuration from our repository(available in the ***tools/kamailio*** folder) as it is.

    * utils.cfg
    * routes.cfg
    * nat.cfg
    * main.cfg
    * kamailio.cfg

## FreeSWITCH

### Installation

#### Debian 11:
```
echo 'deb http://download.opensuse.org/repositories/home:/ganapathi/Debian_11/ /' | sudo tee /etc/apt/sources.list.d/home:ganapathi.list
curl -fsSL https://download.opensuse.org/repositories/home:ganapathi/Debian_11/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_ganapathi.gpg > /dev/null
sudo apt -y update
sudo apt -y install freeswitch freeswitch-meta-flexydial freeswitch-mod-lua  freeswitch-mod-shout  freeswitch-mod-xml-curl freeswitch-mod-xml-rpc
cp /usr/share/freeswitch/conf/flexydial /etc/freeswitch/ -r
```

#### Ubuntu 20.04:
```
echo 'deb http://download.opensuse.org/repositories/home:/ganapathi/xUbuntu_20.04/ /' | sudo tee /etc/apt/sources.list.d/home:ganapathi.list
curl -fsSL https://download.opensuse.org/repositories/home:ganapathi/xUbuntu_20.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_ganapathi.gpg > /dev/null
sudo apt -y update
sudo apt -y install freeswitch freeswitch-meta-flexydial freeswitch-mod-lua  freeswitch-mod-shout  freeswitch-mod-xml-curl freeswitch-mod-xml-rpc
cp /usr/share/freeswitch/conf/flexydial /etc/freeswitch/ -r
```

#### Redhat-8:

```
cat <<EOT > /etc/yum.repos.d/flexydial.repo
[Flexydial_Repo]
name=Flexydial Repo - RHEL-\$releasever-\$basearch
baseurl=http://flexy-repo.s3-website-us-east-1.amazonaws.com/rhel/\$releasever/\$basearch
enabled=1
gpgkey=http://flexy-repo.s3-website-us-east-1.amazonaws.com/RPM-GPG-KEY-ganapathi
gpgcheck=1
EOT
sudo dnf install freeswitch-config-flexydial -y
sudo systemctl enable freeswitch
sudo systemctl start freeswitch
```

### Configuration

1. Add ODBC connection to FIFO, VoiceMail, SIP Profiles(Internal  External). Make sure Freeswitch Database is created on the database server before mentioning it here.

      * /etc/freeswitch/sip_profiles/internal.xml
      * /etc/freeswitch/sip_profiles/external.xml
      * /etc/freeswitch/autoload_configs/fifo.conf.xml
      * /etc/freeswitch/autoload_configs/voicemail.conf.xml

      ```
      <param name="odbc-dsn" value="pgsql://hostaddr=127.0.0.1 port=5432 dbname=freeswitch user=freeswitch password='configme' options='-c client_min_messages=NOTICE'"/>
      ```
2. ODBC Connection to freeswitch core-db as well to move the core database from SQlite to Postgresql or suitable database server according to our needs. where we have postgresql server in our application setup, hence we have created one more database in the name of freeswitch and started using the same.

      * /etc/freeswitch/autoload_configs/switch.conf.xml
      ```
      <param name="core-db-dsn" value="pgsql://hostaddr=127.0.0.1 port=5432 dbname=freeswitch user=freeswitch password='configme' options='-c client_min_messages=NOTICE'" />
      ```

3. Assign Server ID and another ODBC variable on vars.xml, so that it would be used by the call center module dynamically using xml_curl functionalities.

    * /etc/freeswitch/vars.xml

    ```
    <X-PRE-PROCESS cmd="set" data="SERVER_ID=fs001"/>
    <X-PRE-PROCESS cmd="set" data="CC_DSN=pgsql://hostaddr=127.0.0.1 dbname=freeswitch user=freeswitch password='configme' options='-c client_min_messages=NOTICE' application_name='freeswitch'"/>
    ```


## Database Configuration
Due to the initial stage, these new additional tables and data are not integrated with our application. So until then kindly create those tables on the necessary database for smoothing functionalities of Kamailio setup.

### MySQL Database Changes:

1. Create a Dispatcher table if not exists on the Kamailio MySQL database.

``` {.mysql}
CREATE TABLE `dispatcher` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `setid` int(11) NOT NULL DEFAULT 0,
  `destination` varchar(192) NOT NULL DEFAULT '',
  `flags` int(11) NOT NULL DEFAULT 0,
  `priority` int(11) NOT NULL DEFAULT 0,
  `attrs` varchar(128) NOT NULL DEFAULT '',
  `description` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf16;
```
2. Insert table entry on dispatcher table for each Freeswitch Server along with SIP port listening on FreeeSWITCH Server.

``` {.mysql}
INSERT INTO `dispatcher` (`id`, `setid`, `destination`, `flags`, `priority`, `attrs`, `description`)
VALUES
	(1,1,'sip:44.205.255.157:45060',1,1,'',''),
	(2,1,'sip:34.207.122.11:45060',1,1,'','');
```

3. Login into Kamailio Server and reload kamailio dispatcher using below command.

```
kamailio dispatcher reload
```

4. Verify whether all the freeswitch servers are active on the Kamailio dispatcher module or not.

      ```
      kamailio dispatcher dump
      ```
    Where Flag -> AP indicates as active. A:active, I:inactive, T:trying, D:disabled, P: probing mode


### PostgreSQL Database Changes:

1. Login into PostgreSQL CLI and create a freeswitch database and a new freeswitch user for separate login access for freeswitch alone.
According to the Environment PostgreSQL CLI login access may vary, So find a suitable way to login into the PostgreSQL CLI to execute these steps.

```
sudo -u postgres psql -p 5432
postgres=# create database freeswitch;
postgres=# create user freeswitch with password 'configme';
postgres=# grant all privileges on database freeswitch to freeswitch;
```
1. Create Agents Table on freeswitch database(PostgreSQL)

``` {.psql}
CREATE TABLE public.agents (
    name character varying(255),
    instance_id character varying(255),
    uuid character varying(255),
    type character varying(255),
    contact character varying(1024),
    status character varying(255),
    state character varying(255),
    max_no_answer integer DEFAULT 0 NOT NULL,
    wrap_up_time integer DEFAULT 0 NOT NULL,
    reject_delay_time integer DEFAULT 0 NOT NULL,
    busy_delay_time integer DEFAULT 0 NOT NULL,
    no_answer_delay_time integer DEFAULT 0 NOT NULL,
    last_bridge_start integer DEFAULT 0 NOT NULL,
    last_bridge_end integer DEFAULT 0 NOT NULL,
    last_offered_call integer DEFAULT 0 NOT NULL,
    last_status_change integer DEFAULT 0 NOT NULL,
    no_answer_count integer DEFAULT 0 NOT NULL,
    calls_answered integer DEFAULT 0 NOT NULL,
    talk_time integer DEFAULT 0 NOT NULL,
    ready_time integer DEFAULT 0 NOT NULL,
    external_calls_count integer DEFAULT 0 NOT NULL
);
ALTER TABLE public.agents OWNER TO flexydial;
```

2. Create Members table on freeswitch database(PostgreSQL)

``` {.psql}
CREATE TABLE public.members (
    queue character varying(255),
    instance_id character varying(255),
    uuid character varying(255) DEFAULT ''::character varying NOT NULL,
    session_uuid character varying(255) DEFAULT ''::character varying NOT NULL,
    cid_number character varying(255),
    cid_name character varying(255),
    system_epoch integer DEFAULT 0 NOT NULL,
    joined_epoch integer DEFAULT 0 NOT NULL,
    rejoined_epoch integer DEFAULT 0 NOT NULL,
    bridge_epoch integer DEFAULT 0 NOT NULL,
    abandoned_epoch integer DEFAULT 0 NOT NULL,
    base_score integer DEFAULT 0 NOT NULL,
    skill_score integer DEFAULT 0 NOT NULL,
    serving_agent character varying(255),
    serving_system character varying(255),
    state character varying(255)
);

ALTER TABLE public.members OWNER TO flexydial;
```

3. Create Tiers table on freeswitch database(PostgreSQL)

``` {.psql}
CREATE TABLE public.tiers (
    queue character varying(255),
    agent character varying(255),
    state character varying(255),
    level integer DEFAULT 1 NOT NULL,
    "position" integer DEFAULT 1 NOT NULL
);

ALTER TABLE public.tiers OWNER TO flexydial;
```

4. Create subscriber view from existing users table on flexydial database(PostgreSQL)

``` {.psql}
CREATE OR REPLACE VIEW public.subscriber
 AS
 SELECT callcenter_uservariable.extension AS username,
    callcenter_uservariable.device_pass AS password,
    django_site.domain,
    ''::text AS ha1,
    ''::text AS ha1b
   FROM callcenter_uservariable
     JOIN django_site ON callcenter_uservariable.domain_id = django_site.id;

ALTER TABLE public.subscriber
    OWNER TO flexydial;
```