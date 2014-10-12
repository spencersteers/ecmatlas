ECM Atlas 2015
==============
ECM Atlas Django server for Senior Design 2015.


### Setup

MySQL user should be root/1234


Create database
```bash
mysql -u root -p
1234
```

```sql
CREATE DATABASE ecmatlas_2015;
```

Init Django models
```bash
python manage.py syncdb
```

Start the server!
```bash
python manage.py runserver
```


