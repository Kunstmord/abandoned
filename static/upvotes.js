

$(document).ready(function() {
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
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function createCookie(name, value, days) {
        var expires;

        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toGMTString();
        } else {
            expires = "";
        }
        document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + expires + "; path=/";
    }

    var upvote_button = $("#upvote_button");
    var prj_upvotes = $("#prj_upvotes");
    var voted = 0;
    var prj_id = $("#prj_id_div").text();

    if (getCookie(prj_id) == 1) {
        voted = 1;
        upvote_button.html('Thank you for voting');
    }

    upvote_button.click(function() {
        if (voted == 0) {
           $.ajax({
                type: "POST",
                url: '/upvote/',
                data: {'id': upvote_button.data()['projectId']},
                success: function(data) {
                    prj_upvotes.html(data['upvotes']);
                    upvote_button.html('Thank you for voting');
                    voted = 1;
                    createCookie(prj_id, 1, 201);
                }
            });
        }
    });
});