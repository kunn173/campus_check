$(document).ready(function() {
    $('#search').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: '{% url "universities:search_suggestions" %}',
                data: {'term': request.term},
                dataType: 'json',
                success: function(data) {
                    var suggestions = data.universities.concat(data.courses, data.cities);
                    response(suggestions);
                },
            });
        },
        minLength: 2,
        select: function(event, ui) {
            $('#search').val(ui.item.value);
            $('#search-form').submit();
        },
    });
});
