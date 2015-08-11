$(document).ready(function(){
    $('.ch').click(function(){
        var data;
        data = $(this).attr('dt');
        $.get('/faultcorrect/', {data: data});//сделать передачу через post
        show1();
    });
    $('.del_lift').click(function(){
        var data;
        data = $(this).attr('dl');
        $.get('/liftdel/', {data: data});//сделать передачу через post
        show1();

    });
});
function show1(){
    $.ajax({
        url: '/newpost/0/',
        cache: false,
        success: function(html){
            $(".fi-check").html(html);
        }
    });
}   

// $(document).on('close.fndtn.alert', function(event) {
//   console.info('An alert box has been closed!');
// });

// $(".datepickerTimeField").datepicker({
//         changeMonth: true,
//         changeYear: true,
//         dateFormat: 'dd.mm.yyyy',
//         firstDay: 1, changeFirstDay: false,
//         navigationAsDateFormat: false,
//         duration: 0,// отключаем эффект появления
// });