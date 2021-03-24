# sCool Learning Analytics application


Run me : 

```
docker run -p 5000:5000 aniltilanthe/scool-la-app
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
