# ECM Atlas - 2014

Last years project


## Setting up database

MySQL user should be root/1234

```sql
CREATE DATABASE ecmatlas;
```

Use the most recent `ecmatlas.mysql` file and restore the database.
```bash
mysql -u root -p1234 ecmatlas < ecmatlas.mysql
```

Start the server!
```bash
python manage.py runserver
```