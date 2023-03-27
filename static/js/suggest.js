$(document).ready(function() {
    $('#search').on('input', function() {
        var search_term = $(this).val();
        if (search_term.length >= 2) {
            var url = $('#search').data('url');
            $.ajax({
                url: url,
                data: {'term': search_term},
                dataType: 'json',
                success: function(data) {
                    var suggestions = data.universities.concat(data.courses, data.cities);
                    $('#search').autocomplete({
                        source: suggestions,
                        minLength: 2,
                        select: function(event, ui) {
                            $('#search').val(ui.item.value);
                            $('#search-form').submit();
                        }
                    });
                },
            });
        }
    });
});


