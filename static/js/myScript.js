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
$(".datepickerTimeField").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'dd.mm.yyyy',
        firstDay: 1, changeFirstDay: false,
        navigationAsDateFormat: false,
        duration: 0,// отключаем эффект появления
});