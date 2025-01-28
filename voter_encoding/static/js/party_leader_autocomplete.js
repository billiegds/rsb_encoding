(function($) {
    $(document).ready(function() {
        // When the party leader input field is focused or a key is typed
        $('#party_leader').autocomplete({
            source: function(request, response) {
                // Send the query to Django admin view
                $.ajax({
                    url: '/admin/voter_encoding/party-leader-autocomplete/',  // Your custom view URL
                    data: {
                        'q': request.term
                    },
                    success: function(data) {
                        response(data.map(function(item) {
                            return {
                                label: item.name,  // Name to display in the list
                                value: item.name,   // Value to set the field with
                                id: item.id         // ID to set in the hidden field
                            };
                        }));
                    }
                });
            },
            minLength: 2,  // Start searching after 2 characters
            select: function(event, ui) {
                // Update input field and hidden ID field
                $('#party_leader').val(ui.item.value);  // Set the name
                $('#party_leader_id').val(ui.item.id);  // Set the selected ID (hidden field)
            }
        });
    });
})(django.jQuery);
