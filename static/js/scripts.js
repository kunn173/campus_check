$('#search-input').keyup(function() {
  var query;
  query = $(this).val();
  $.get('/universities/suggest/',
    {'suggestion': query},
    function(data) {
      $('#categories-listing').html(data);
      })
});
