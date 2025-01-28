from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import VotersList, PartyLeader, Supporters, Cluster
from django.contrib import messages  # For flash messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from django.http import HttpResponse

def voters_autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        results = VotersList.objects.filter(name__icontains=query).values('id', 'name', 'precinct_number', 'legend', 'address', 'barangay')
        return JsonResponse(list(results), safe=False)
    return JsonResponse([], safe=False)

@login_required
def add_party_leader(request):
    party_leaders = PartyLeader.objects.all()  # Get all party leaders
    if request.method == 'POST':
        party_leader_name = request.POST.get('party_leader')
        cluster = request.POST.get('cluster')
        precinct = request.POST.get('precinct')
        legend = request.POST.get('legend')
        address = request.POST.get('address')
        barangay = request.POST.get('barangay')
        contact_number = request.POST.get('contact_number')

        # Check if the party leader with the exact name already exists
        existing_party_leader = PartyLeader.objects.filter(party_leader_name__iexact=party_leader_name).first()
        print(f"Existing Leader: {existing_party_leader}")
        # Check if the supporter with the exact name already exists
        existing_supporter = Supporters.objects.filter(supporter_name__iexact=party_leader_name).first()
        print(f"Existing Supporter: {existing_supporter}")

        if existing_party_leader:
            # If exists, show a message and do not save again
            messages.warning(request, 'This Party Leader already exists in the Party Leaders DB.')
            return JsonResponse({
                'status': 'warning',
                'message': 'This Party Leader already exists in the Party Leaders DB.',
                'show_notification': True
            })  # Redirect to the add party leader page
        if existing_supporter:
            # If exists, show a message and do not save again
            messages.warning(request, 'This Party Leader already exists in the Supporters DB.')
            return JsonResponse({
                'status': 'warning',
                'message': 'This Party Leader already exists in the Supporters DB.',
                'show_notification': True
            })  # Redirect to the add party leader page
        print(cluster)
        # Create a new PartyLeader entry
        PartyLeader.objects.create(
            party_leader_name=party_leader_name,
            party_leader_cluster=cluster,    
            precinct_number=precinct,
            legend=legend,
            address=address,
            barangay=barangay,
            contact_number=contact_number,
        )

        # Success message
        messages.success(request, 'Party Leader added successfully!')
         # Return success response
        return JsonResponse({
            'status': 'success',
            'message': 'Party Leader added successfully!',
            'clear_fields': True
        })
        
    return render(request, 'add_party_leader.html', {
        'party_leaders': party_leaders,  # This is how you pass the queryset to the template
    })
    
def party_leader_list(request):
    party_leaders = PartyLeader.objects.all()  # Retrieve all party leaders from the database
    
    # Ensure you're passing the context correctly to the template
    return render(request, 'add_party_leader.html', {
        'party_leaders': party_leaders,  # This is how you pass the queryset to the template
    })
    
def autocomplete_supporter(request):
    query = request.GET.get('q', '')
    if query:
        supporters = Supporters.objects.filter(name__icontains=query)  # Filter by name
        results = [{"name": supporter.name, "precinct": supporter.precinct, "address": supporter.address} for supporter in supporters]
    else:
        results = []
    return JsonResponse(results, safe=False)

@login_required
def add_supporter(request):
    supporters = Supporters.objects.all()  # Get all supporters
    if request.method == 'POST':
        supporter_name = request.POST.get('party-supporters')
        print(f"Supporter Name from form: '{supporter_name}'")

        # Check if the supporter with the exact name already exists
        existing_supporter = Supporters.objects.filter(supporter_name__iexact=supporter_name).first()
        print(f"Existing Supporter: {existing_supporter}")

        existing_leader = PartyLeader.objects.filter(party_leader_name__iexact=supporter_name).first()
        print(f"Existing Leader: {existing_leader}")
        
        # Check if the supporter already exists in either model
        if existing_supporter:
            messages.warning(request, 'This Supporter already exists in the Supporter DB.')
            return JsonResponse({
                'status': 'warning',
                'message': 'This Supporter already exists in the Supporter DB.',
                'show_notification': True
            })  # Send warning message as a JSON response
            
        if  existing_leader:
            messages.warning(request, 'This Supporter already exists in the Party Leader DB.')
            return JsonResponse({
                'status': 'warning',
                'message': 'This Supporter already exists in the Party Leader DB.',
                'show_notification': True
            })  # Send warning message as a JSON response
        
        # Now, this code should not be reached if supporter exists
        # Create a new Supporter entry
        Supporters.objects.create(
            
            supporter_name=supporter_name,
            supporter_barangay=request.POST.get('barangay_supporter'),
            supporter_address=request.POST.get('address_supporter'),
            supporter_contact_number=request.POST.get('contact_number_supporter'),
            supporter_precinct_number=request.POST.get('precinct_supporter', '0000'),
            supporter_cluster = request.POST.get('cluster_supporter'),# default value
            party_leader=request.POST.get('party_leader'),
            party_barangay=request.POST.get('barangay', 'Not Provided'),
            party_address=request.POST.get('address'),
            party_contact_number=request.POST.get('contact-number'),
            party_precinct_number=request.POST.get('precinct', '0000'),  # default value
            party_cluster_id=request.POST.get('cluster'),
            party_legend=request.POST.get('legend'),
            supporter_legend=request.POST.get('legend_supporter')
        )
        messages.success(request, 'Supporter added successfully!')
        
        return render(request, 'add_supporter.html', {
            'supporters': supporters,  # Pass the list of all supporters to the template
        })
    
    return render(request, 'add_supporter.html', {
        'supporters': supporters,  # Pass the list of all supporters to the template
    })

def party_leader_autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        results = PartyLeader.objects.filter(
            party_leader_name__icontains=query).values(
                'party_leader_name', 'precinct_number', 
                'legend', 'address', 'barangay', 'contact_number', 'party_leader_cluster')
        return JsonResponse(list(results), safe=False)
    return JsonResponse([], safe=False)



def supporters_list(request):
    # Retrieve all supporters from the database
    supporters = Supporters.objects.all()
    return render(request, 'supporters_list.html', {'supporters': supporters})

@login_required
def view_list(request):
    # Retrieve all supporters from the database
    voters = VotersList.objects.all()
      # Paginate the list
    paginator = Paginator(voters, 25)  # Show 10 voters per page
    page_number = request.GET.get('page')  # Get current page from the URL
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})

def party_leader_list_ajax(request):
    search_query = request.GET.get('search[value]', '')  # Get the search query
    start = int(request.GET.get('start', 0))  # Pagination start index
    length = int(request.GET.get('length', 10))  # Pagination length (items per page)
    
    # Get the voters from the database
    voters = VotersList.objects.all()

    # Apply search query filter using Q objects
    if search_query:
        # Using Q objects for OR logic in filtering
        search_filter = Q(name__icontains=search_query) | \
                        Q(precinct_number__icontains=search_query) | \
                        Q(address__icontains=search_query) | \
                        Q(barangay__icontains=search_query)
        
        # Apply filter to voters queryset
        voters = voters.filter(search_filter)
    
    # Paginate the voters list
    paginator = Paginator(voters, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)
    
    # Prepare the response data
    data = {
        'draw': int(request.GET.get('draw', 1)),  # For DataTables
        'recordsTotal': paginator.count,  # Total number of records before filtering
        'recordsFiltered': paginator.count,  # Total number of records after filtering (search applied)
        'data': [
            {
                'name': voter.name,
                'precinct_number': voter.precinct_number,
                'legend': voter.legend,
                'address': voter.address,
                'barangay': voter.barangay
            }
            for voter in page_obj
        ],
    }

    return JsonResponse(data)


def find_cluster_by_precinct(request):
    query = request.GET.get('precinct_number', '').strip()
    query = query.lstrip("0")
    if query:
        # Check for cluster matching manually, as the `__contains` lookup doesn't work in SQLite
        matching_cluster = None
        for cluster in Cluster.objects.all():
            if query in cluster.items:  # Assuming items is a list-like field on the cluster
                matching_cluster = cluster
                break
        
        # If no matching cluster is found, return an error message
        if matching_cluster:
            result = {"cluster_id": matching_cluster.cluster_id}
        else:
            result = {"error": "No matching cluster found."}
        
        return JsonResponse(result)

    return JsonResponse({"error": "Precinct number not provided."})


@login_required
def index(request):
    return render(request, 'login.html')


import uuid
from openpyxl import Workbook
from django.http import HttpResponse
from .models import Supporters

def export_supporters(request):
    # Create a workbook and add a worksheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Supporters'

    # Define the headers for the columns
    headers = [
        "Voter ID", "Supporter Cluster", "Supporter Name", 
        "Supporter Barangay", "Supporter Address", "Supporter Contact Number", 
        "Supporter Precinct Number", "Supporter Legend",
        "Party Leader", "Party Cluster ID", "Party Precinct Number", 
        "Party Barangay", "Party Address", "Party Contact Number", 
        "Party Precinct Number", "Party Legend"
    ]
    
    # Write headers to the first row
    sheet.append(headers)

    # Query the Supporters table
    supporters = Supporters.objects.all()

    # Add data rows to the sheet
    for supporter in supporters:
        row = [
            supporter.voter_id,
            supporter.supporter_cluster,
            supporter.supporter_name,
            supporter.supporter_barangay,
            supporter.supporter_address,
            supporter.supporter_contact_number,
            supporter.supporter_precinct_number,
            supporter.supporter_legend,
            supporter.party_leader,
            supporter.party_cluster_id,
            supporter.party_precinct_number,
            supporter.party_barangay,
            supporter.party_address,
            supporter.party_contact_number,
            supporter.party_precinct_number,
            supporter.party_legend
        ]
        sheet.append(row)

    
    # Set the response for downloading the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # Make sure it's forced as an attachment and not inline
    response['Content-Disposition'] = 'attachment; filename="supporters.xlsx"'
    
    # Ensure no caching
    response['Cache-Control'] = 'no-cache'

    # Save the workbook to the response
    workbook.save(response)

    return response

def export_party_leaders(request):
    # Create a workbook and add a worksheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Party Leaders'

    # Define the headers for the columns
    headers = [
        "Party Leader Cluster", "Party Leader Name", "Precinct Number", 
        "Legend", "Address", "Barangay", "Contact Number"
    ]
    
    # Write headers to the first row
    sheet.append(headers)

    # Query the PartyLeader table
    party_leaders = PartyLeader.objects.all()

    # Add data rows to the sheet
    for leader in party_leaders:
        row = [
            leader.party_leader_cluster,
            leader.party_leader_name,
            leader.precinct_number,
            leader.legend if leader.legend else 'Not Provided',
            leader.address,
            leader.barangay,
            leader.contact_number
        ]
        sheet.append(row)

    # Set the response for downloading the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # Make sure it's forced as an attachment and not inline
    response['Content-Disposition'] = 'attachment; filename="party_leaders.xlsx"'
    
    # Ensure no caching
    response['Cache-Control'] = 'no-cache'

    # Save the workbook to the response
    workbook.save(response)

    return response