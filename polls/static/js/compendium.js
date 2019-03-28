$(document).ready( function () {
var csrftoken = Cookies.get('csrftoken');
    $('.like').click(
    function(e){
       $.get('/polls/save_like', { coment: $(this).name }, function() {
});
});
});