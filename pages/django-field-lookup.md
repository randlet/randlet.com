title:  Looking up Django model fields from strings
date: 2015-02-16
tags: [python, django]
blurb:  A short snippet for finding model fields from Django lookup strings.
thumbnail: lookup.jpg
attribution: http://www.flickr.com/photos/opendemocracy/2871333638/

I recently needed to take Django field lookup/query strings and
find out what model field they were referencing.  For example, imagine
we have the following models:


    :::python
    class Business(models.Model):

        name = models.CharField(max_length=255)
        business_type = models.IntegerField(choices=zip(range(5), range(5)), default=1)


    class Department(models.Model):

        name = models.CharField(max_length=255)
        business = models.ForeignKey(Business)


    class Staff(models.Model):

        first_name = models.CharField(max_length=255, help_text=_("Enter the name of the staff being rounded"))
        last_name = models.CharField(max_length=255, help_text=_("Enter the name of the staff being rounded"))

        department = models.ForeignKey(Department)



I needed a function that would take a string like
`department__business__business_type` and return
the Business.name
`<django.db.models.fields.IntegerField: business_type>`
field (I needed to access the `choices` attribute of fields).

Here's a short function which will do that sort of lookup:

    :::python

    def find_field(cls, lookup):
        """Take a root class and a field lookup string
        and return the model field if it exists or raise
        a django.db.models.fields.FieldDoesNotExist if the
        field is not found."""

        lookups = list(reversed(lookup.split("__")))

        field = None

        while lookups:

            f = lookups.pop()

            # will raise FieldDoesNotExist exception if not found
            field = cls._meta.get_field(f)

            try:
                cls = field.rel.to
            except AttributeError:
                if lookups:
                    # not all lookup fields were used
                    # must be an incorrect lookup
                    raise django.db.models.fields.FieldDoesNotExist(lookup)

        return field

    # use like:
    >> find_field(Staff, "department__business__business_type")
    <django.db.models.fields.IntegerField: business_type>
    >>
    >> find_field(Staff, "department__business__business_type")
    <django.db.models.fields.related.ForeignKey: business>
    >>
    >> find_field(Staff, "department__foo")
    FieldDoesNotExist: Department has no field named 'foo'
    >>


