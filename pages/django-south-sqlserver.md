title: A Couple of Django South & SQL Server Migration Tips
date: 2013-04-23
tags: [python, django, south, sql server, migration]
blurb: Problems and solutions to a couple of issues I ran into using Django South & SQL Server 
thumbnail: south.jpg 
attribution: http://www.flickr.com/photos/theothermattm/251502416

I was recently writing a bunch of [Django South](http://south.aeracode.org)
migrations for a project at work and ran into two problems that caused my
migrations to fail when run against a SQL Server 2008 database (same behaviour
on Microsoft SQL Server 2008R2, SQL Express 2008 &amp; SQL Express 2012). These
were migrations that ran smoothly on both SQLite &amp; PostgreSQL so I had to
modify the migrations to included a little bit of special case code for SQL
Server databases.

I'm going to post the problems &amp; solutions here for myself when I run into
them again in the future, and hopefully someone else will find them useful when
googling for error messages 

** Issue 1: ** `Cannot create new connection because in manual or distributed transaction mode.`

** Issue 2: ** ` Cannot drop the index '...' because it does not exist or you do not have permission` 

##### Issue 1: Cannot create new connection because in manual or distributed transaction mode. #####

The first issue that I ran into was dealing with a data migration that looked something like:

    :::python

    class Migration(DataMigration):

        def forwards(self, orm):
            for obj in orm["someapp.SomeModel"].objects.all():
                obj.foo = "bar"
                obj.save()

        def backwards(self, orm):
            "Write your backwards methods here."

        models = {...}

This worked fine for SQLite and Postgres but running the same migration on
SQL(Server|Express) gave a somewhat cryptic `Cannot create new connection
because in manual or distributed transaction mode.`

A little bit of googling let me to a [Microsoft support
page](http://support.microsoft.com/kb/272358) explaining what the error was
about (SQLOLEDB only allows a single connection within a transaction). It
appears that when interating over the collection above a new connection is
created to retrieve the next object on each iteration. Since this is all
happening withing a single transaction, SQL Server complains.

The simplest solution is just to pull all your objects into memory before
iterating over them by calling `list` on the orm["someapp.SomeModel"].objects.all().

    :::python

    class Migration(DataMigration):

        def forwards(self, orm):
            for obj in list(orm["someapp.SomeModel"].objects.all()):
                obj.foo = "bar"
                obj.save()

        def backwards(self, orm):
            "Write your backwards methods here."

        models = {...}

The major disclaimer here is that if your collection contains a huge number of
objects, you may run into memory limitations. In that case, something more
creative probably needs to be done like splitting your data into batches.

##### Issue 2: Cannot drop the index '...' because it does not exist or you do not have permission #####

The second issue occured when I was trying to alter the max\_length attribute
of a column that had an index on it. So the simplest sort of migration where
this would occur looks like:

    :::python

    class Migration(SchemaMigration):

        def forwards(self, orm):

            db.alter_column('someapp_somemodel', 'field_ame', self.gf('django.db.models.fields.CharField')(max_length=255))

        def backwards(self, orm):
            ...

Again, this worked fine on both SQLite and Postgres but SQLServer complained with an error like:

    :::python
    AttributeError: 'module' object has no attribute 'Migration'

    FATAL ERROR - The following SQL query failed: DROP INDEX [someapp_somemodel_cac2c6] on [dbo].[someapp_somemodel]

    The error was: (-2147352567, 'Exception occurred.', (0, u'Microsoft SQL Server Native Client 10.0', u"Cannot drop the index 'dbo.someapp_somemodel

    .someapp_somemodel_cac2c6', because it does not exist or you do not have permission.", None, 0, -2147217865), None)

    Command:

    DROP INDEX [someapp_somemodel_cac2c6] on [dbo].[someapp_somemodel]

    Parameters:

    []

I couldn't find much on google to point me in the right direction, but if I
dropped the problem index manually in SQL Server Management Studio before
running the migration it would run without any issues.

Luckily South comes with a way to explicitly drop and create indexes during
migrations so I was able to modify my migration to look like:


    :::python

    class Migration(SchemaMigration):

        def forwards(self, orm):
            from south.db import engine

            if 'sql_server' in engine:
                db.drop_index("someapp_somemodel", "column_name")

            db.alter_column('someapp_somemodel', 'comlumn_ame', self.gf('django.db.models.fields.CharField')(max_length=255))

            if 'sql_server' in engine:
                db.create_index("someapp_somemodel", ["column_name"])

        def backwards(self, orm):
            ...

Problem solved!  The migration now runs smoothly on SQLServer, SQL Express, SQLite & Postgres.

I'll write another post some day explaining why I'm stuck using SQLServer for Django projects ;)
