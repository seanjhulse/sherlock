from django.db import models

class Packet(models.Model):
    '''
    A packet represents a generic piece of data sent across a wire. Something with a 
    host ip address (where it came from) and a destination ip address (where it's going).
    It also has a port and some room for the internal data. The data will likely be
    broken up into multiple fields in the future.

    Model fields: https://docs.djangoproject.com/en/3.1/ref/models/fields/
    '''
    
    # IP Address limited to 39 characters
    source_ip_address = models.CharField(max_length=39, null=True)
    destination_ip_address = models.CharField(max_length=39, null=True)
    
    source_host_name = models.CharField(max_length=256, null=True)
    destination_host_name = models.CharField(max_length=256, null=True)

    # Version 
    version = models.CharField(max_length=256, null=True)

    # IP Header Length
    header_length = models.IntegerField(default=0)

    # Time to Live
    ttl = models.CharField(max_length=256, null=True)

    # Protocol
    protocol = models.CharField(max_length=256, null=True)

    # Source and Destination Port limited to 5 characters
    source_port = models.CharField(max_length=5, null=True)
    destination_port = models.CharField(max_length=5, null=True)

    # Sequence Number
    sequence_number = models.CharField(max_length=256, null=True)

    # Acknowledgement
    acknowledgement = models.CharField(max_length=256, null=True)

    # TCP Flags
    flags = models.CharField(max_length=256, null=True)

    # Payload is just an large TextField representing the body of a message
    payload = models.TextField(default=None)

    # Should store when this data was published to the database
    pub_date = models.DateTimeField('date published')

    class Meta:
        managed = True

class Scan(models.Model):
    '''
    Represents the results of an nmap scan.
    '''

    # The scan command that was run
    command = models.TextField(default=None)

    # Results of the scan that was run (stored as JSON)
    scan = models.TextField(default="{}")

    # Should store when this data was published to the database
    pub_date = models.DateTimeField('date published')

    class Meta:
        managed = True