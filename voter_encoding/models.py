from django.db import models
import uuid


# Create your models here.
class Supporters(models.Model):
    
    party_chairman = models.CharField(max_length=100)
    # Basic Voter Information
    voter_id = models.CharField(max_length=20, unique=True)
    supporter_type= models.CharField(max_length=100)
    supporter_cluster = models.CharField(max_length=100)
    supporter_name = models.CharField(max_length=200, unique=True)  # Ensure the name is unique across all voters
    supporter_barangay = models.CharField(max_length=100, null=True, blank=True, default='Not Provided')         # Add
    supporter_address = models.TextField()            # Address of the voter
    supporter_contact_number = models.CharField(max_length=15)  # Contact number with validation length
    supporter_precinct_number = models.CharField(max_length=50, default='0000')  # Default precinct number
    supporter_legend = models.TextField(max_length=20) 
    # Additional Fields for party leader
    party_leader = models.CharField(max_length=200, null=True, blank=True)  # Party leader's name
    party_cluster_id = models.CharField(max_length=100)
    party_precinct_number = models.CharField(max_length=50, default='0000')  # Default precinct number
    party_barangay = models.CharField(max_length=100, null=True, blank=True, default='Not Provided')  # Default barangay
    party_address = models.TextField()            # Address of the voter
    party_contact_number = models.CharField(max_length=15)  # Contact number with validation length
    party_precinct_number = models.CharField(max_length=50, default='0000')  # Default precinct number
    party_legend = models.TextField(max_length=20) 
    def save(self, *args, **kwargs):
        # If a voter_id isn't provided, generate a new one
        if not self.voter_id:
            # You can customize the logic for generating the voter_id
            self.voter_id = f"Supporter-{uuid.uuid4().hex[:8].upper()}"
        super(Supporters, self).save(*args, **kwargs)



    def __str__(self):
        return f"{self.supporter_name} (Precinct {self.supporter_precinct_number}, Barangay {self.supporter_barangay})"
    

class PartyLeader(models.Model):
    party_leader_cluster = models.CharField(max_length=100)
    party_chairman = models.CharField(max_length=100)
    party_leader_name = models.CharField(max_length=200)  # Corrected field name
    precinct_number = models.CharField(max_length=50)
    legend = models.CharField(max_length=100, null=True)
    address = models.TextField()
    barangay = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        
        return self.party_leader_name  # Updated field for string representation


class VotersList(models.Model):
    precinct_number = models.CharField(max_length=50)  # PRECINCT field to store precinct number
    legend = models.CharField(max_length=100, null=True)  # LEGEND field to store the legend of the voter
    name = models.CharField(max_length=200)  # NAME field to store the name of the voter
    address = models.TextField()  # ADDRESS field to store the address of the voter
    barangay = models.CharField(max_length=100)  # BARANGAY field to store the barangay of the voter

    def __str__(self):
        return self.name  # String representation for easy referencing in the admin interface
    
    
class Cluster(models.Model):
    cluster_id = models.CharField(max_length=100)
    items = models.JSONField()  # Use JSONField for lists/arrays

    def __str__(self):
        return self.cluster_id