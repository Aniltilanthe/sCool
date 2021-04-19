# sCool Learning Analytics application


Run me : 

```
docker run -p 8090:8090 aniltilanthe/scool-la-app
```


also further options try these:-

```
#map localhost:8090 to the container 8090        -    127.0.0.1 is the localhost
docker run -d -p 127.0.0.1:8090:8090 aniltilanthe/scool-la-app
```

OR

```
#1 Automatically publish all ports exposed by container and binds them to random port on the host machine
docker container run -P -d aniltilanthe/scool-la-app

#2.a Find the host machine port using container_uuid
docker container port *insert container_uuid*

#2.b Or using netstat
netstat -ntlp
```

check localhost

```
curl -I 0.0.0.0:8090

#or
curl -v 0.0.0.0:8090
```

Build me: 

```
docker build -t aniltilanthe/scool-la-app .
```

Clone me from docker hub :  

```
docker pull aniltilanthe/scool-la-app
```

Docker hub repo :  

* aniltilanthe/scool-la-app






sCool Data analysis and visualization


* Installation

```
pip install -r requirements.txt
```



* Set Up

  - Change the Database name (**DatabaseName**) in **constants.py**




* Login Redirect form

```
<form action="http://127.0.0.1:8888/login?securityStamp=<'securityStampString'>" method="post">
  <input type="submit" value="sCool Data Visualization">
</form>
```
