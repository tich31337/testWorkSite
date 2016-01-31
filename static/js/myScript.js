$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.ch').click(function () {
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
    $('.fredact').click(function () {
        var fdata;
        fdata = $(this).attr('dt');
        $.ajax({
                url: '/newpost/',
                data: {data: fdata},
                success: function () {
                    $(html).load('/newpost/', {
                        data: fdata
                    });
                }
            })
            .done(function () {
                console.log("success");
            })
            .fail(function () {
                console.log("error");
            })
            .always(function () {
                console.log("complete");
            });
    });
    $('.del_lift').click(function () {
        var data;
        data = $(this).attr('dl');
        $.get('/liftdel/', {data: data});//сделать передачу через post
        location.reload();
        // $('.main').load(location.href+" .main>*","");
        // show1();

    });

    // Валидация IP адреса

    $('.chMil').click(function () {
        var dtUser, dtIP;
        var ob = $(this);
        dtUser = ob.attr('dtUser');
        dtIP = ob.attr('dtIP');
        $.ajax({
            url: '/validip/',
            type: "POST",
            data: {dtUser: dtUser, dtIP: dtIP},
            success: function () {
                ob.toggleClass('chk nochk');
            }
        })
    });
});
function show1() {
    $.ajax({
        url: '/newpost/0/',
        cache: true,
        success: function (html) {
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