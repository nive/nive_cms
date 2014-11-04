/*
Alternative link actions
-----------------------------
Turns editor actions links into ajax calls and handles responses based on the content and
information returned. HTML documents are opened in modal windows, triggers redirects, and shows messages
if refresh = false returned by the server.
To activate just add `rel="niveAction"` as attribute to a link (a).

Example: ::

  <a href="page/moveup" rel="niveAction">Move page up</a>

*/
(function ($) {
    var _settings = {
        id: 'callaction',
        src: function (sender) {
            return jQuery(sender).attr('href');
        }
    };

    $.niveAction= function (id) {
        if (id) $(id + " a[rel^='niveAction']").attr("onClick", "$(this).callaction(); return false;");
        else    $("a[rel^='niveAction']").attr("onClick", "$(this).callaction(); return false;");
    };
    $.callaction = function () {
        return "";
    };
    $.fn.callaction = function () {
        var href = jQuery(this).attr('href');
        $.ajax(href)
            .done($(this).nive_actiondelegation)
            .fail(function(jqXHR, message, error)   { console.log(message); });
    };
    $.fn.nive_actiondelegation = function (data, message, jdXHR) {
        var loc = data.location || jdXHR.getResponseHeader('X-Relocate');
        if (data.refresh || data.refresh==undefined) {
            if(window!=window.top) return window.parent.close(loc);
            if (loc) {
                // avoid unnamed view redirects
                if (loc.indexOf("@") == -1) {
                    if (loc.match("\.html$"))
                        loc = loc.substring(0, loc.length - 5);
                    loc += "/@view";
                }
                location.href = loc;
            }
            else
                location.href = location.href;
        }
    }

})(jQuery);

$(document).ready(function(){
  $.niveAction();
});


(function ($) {
    $.fn.editblocks = function( ) {
        // reusing editblock widgets. ignore stop event.
        this.stopEvent = function(event) {};
        return this;
    }
})(jQuery);
