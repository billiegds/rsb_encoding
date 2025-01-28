from django.utils import timezone
from django.contrib import admin
from .models import Supporters, PartyLeader, VotersList, Cluster


@admin.register(Supporters)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('supporter_name', 'supporter_precinct_number', 'supporter_barangay', 'supporter_contact_number', 'party_leader')  # Use safe_encoding_date
    search_fields = ('supporter_name', 'supporter_precinct_number', 'party_leader')
    list_filter = ('party_leader', 'supporter_barangay', )

@admin.register(PartyLeader)
class PartyLeaderAdmin(admin.ModelAdmin):
    list_display = ('party_leader_name', 'precinct_number', 'barangay', 'contact_number')  # Use safe_encoding_date
    search_fields = ('barangay', 'precinct_number')
    list_filter = ('precinct_number', 'barangay',)
@admin.register(VotersList)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('precinct_number', 'legend', 'name', 'address', 'barangay')
    search_fields = ('precinct_number', 'legend', 'name', 'address', 'barangay')
    
@admin.register(Cluster)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('cluster_id', 'items')