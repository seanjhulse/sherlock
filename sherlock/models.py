from django.db import models

class Packet(models.Model):
    '''
    A packet represents a generic piece of data sent across a wire. Something with a 
    host ip address (where it came from) and a destination ip address (where it's going).
    It also has a port and some room for the internal data. The data will likely be
    broken up into multiple fields in the future.

    Model fields: https://docs.djangoproject.com/en/3.1/ref/models/fields/
    '''
    
    # IP Address limited to 39 characters (rounded up)
    host_ip_address = models.CharField(max_length=39)
    dest_ip_address = models.CharField(max_length=39)

    # Port limited to 5 characters
    port = models.CharField(max_length=5)

    # Data is just an "unlimited" TextField
    data = models.TextField

    # Should store when this data was published to the database
    pub_date = models.DateTimeField('date published')