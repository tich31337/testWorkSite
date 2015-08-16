$(document).ready(function(){
    $('.ch').click(function(){
        var data;
        data = $(this).attr('dt');
        $.get('/faultcorrect/', {data: data});//сделать передачу через post
        location.reload();
        // show1();
    });
    // $('.fredact')click(function() {
    //     var fdata;
    //     fdata = $(this).attr('dt');
    //     $.get('/newpost/', {data: data});
    //     location.reload();
    // });
    $('.fredact').click(function(){
        var fdata;
        fdata = $(this).attr('dt');
        $.ajax({
        url: '/newpost/',
        data: {data: fdata},
        success: function(){
            $(html).load('/newpost/',{
            data: fdata});
            }
    })
    .done(function() {
        console.log("success");
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        console.log("complete");
    });
    });
    $('.del_lift').click(function(){
        var data;
        data = $(this).attr('dl');
        $.get('/liftdel/', {data: data});//сделать передачу через post
        location.reload();
        // $('.main').load(location.href+" .main>*","");
        // show1();

    });
});
function show1(){
    $.ajax({
        url: '/newpost/0/',
        cache: true,
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