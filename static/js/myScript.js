$(document).ready(function(){
    $('.ch').click(function(){
        var data;
        data = $(this).attr('dt');
        $.get('/faultcorrect/', {data: data});
        show();
    });
});
function show(){
    $.ajax({
        url: '/newpost/0/',
        cache: true,
        success: function(html){
            $("#main").html(html);
        }
    });   
}