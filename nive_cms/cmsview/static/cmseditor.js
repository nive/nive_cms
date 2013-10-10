
/*
Cms edit blocks
---------------
Handles the small edit editbars attached to page elements, columns and pages.
Uses cookies to store settings between page relods.

*/
(function ($) {
      
    var _settings = {
        enabled: true,
        useCookies: true,
        editblockPrefix: "#nive-editblock",
        elementPrefix: "#nive-element",
        editblockViewUrl: "editblock"
    }

	$(document).ready(function(){
	    // load current setting from cookie
	    if(_settings.useCookies) {
		    var v=$.cookie("peEnabled");
		    if(v!=null) _settings.enabled=v=="true"?true:false;
		}
	    _settings.enabled=!_settings.enabled;
	    $.fn.editblocks().enable();
	    // patch pagelement links to handle overlaying clicks.
	    // intercept and disable content if ctrl key is pressed links. 
	    $('.pageelement a').click(function() {
	        if(_settings.enabled) {
	            event = arguments[0];
	            if(event && !event.ctrlKey)  return;
	            $(this).parent().click();
	            return false;
	        }
	    });
	});
	
	
	$.fn.editblocks = function( ) {

		this.enable = function() {
		  _settings.enabled = _settings.enabled ? false:true;
		  $.cookie("peEnabled", _settings.enabled, { path: '/' });
		  if(_settings.enabled) {
		    $('#peMenuEditOn').hide();
		    $('#peMenuEditOff').show();
		  } else {
		    $('#peMenuEditOn').show();
		    $('#peMenuEditOff').hide();
		    //this.peHideAll();
		  }
		  $('.pageelement').each( function(index) {
		    if(_settings.enabled)  $(this).hasClass("peBox") ?    $(this).addClass("peBox_ov") :    $(this).addClass("pageelement_ov");
		    else                   $(this).hasClass("peBox_ov") ? $(this).removeClass("peBox_ov") : $(this).removeClass("pageelement_ov");
		  });
		  $('.pageeditorEditblock').each( function(index) {
		    _settings.enabled ? $(this).show() : $(this).hide();
		  });
		}
		
		this.showBlock = function(blockid) {
		  $(blockid).show('slow');
		}
		
		this.hideBlock = function(blockid) {
		  $(blockid).hide('slow');
		}
		
		this.loadToggleBlock = function(url, blockid) {
		  ref = $(blockid);
		  if(ref.html()=="") { ref.load(url, function(){ ref.toggle('fast'); $.niveOverlay(blockid);}); return; }
		  ref.toggle('fast');
		}
		
		this.toggleBlock = function(blockid) {
		  $('.pageeditorEditblockElement').each( function(index) {
		    if("#"+$(this).attr("id")!=blockid) $(this).hide('fast');
		  });
		  $(blockid).toggle('fast');
		}
		
		this.hideAll = function() {
		  $('.pageeditorEditblockElement').each( function(index) {
		    $(this).hide('fast');
		  });
		}
		
		this.toggleMenu = function(blockid, event, hideBlockid) {
		  $(hideBlockid).hide('fast');
		  $(blockid).toggle('fast');
		}
		
		this.stopEvent = function(event) {
		  if(!_settings.enabled) return false;
		  if( event.stopPropagation ) { event.stopPropagation(); } 
		  else { event.cancelBubble = true; } // IE
		}
		
		/* page element functions */
		
		this.clickAndLoadElement = function(id, path, event) {
		  if(!_settings.enabled) return false;
		  this.stopEvent(event);
		  var eid = _settings.editblockPrefix+id;
		  var eblock = $(eid);
		  if(eblock.html()==undefined) {
		      $.get(path+_settings.editblockViewUrl, 
		            function(data) { 
		                 $(_settings.elementPrefix+id).prepend(data); 
		                 $(this).toggleBlock(eid);
		                 $.niveOverlay(eid); 
		             }).error(function(jqXHR, textStatus, errorThrown) { /*alert("?"); errorThrown*/ });
		  }
		  else this.toggleBlock(eid);
		}
		
		this.clickElement = function(id, event) {
		  if(!_settings.enabled) return false;
		  this.stopEvent(event);
		  this.toggleBlock(_settings.editblockPrefix+id);
		}
		
		this.dblClickElement = function(id, event) {
		  if(!_settings.enabled) return false;
		  this.stopEvent(event);
		  this.toggleBlock(_settings.editblockPrefix+id);
		}
		return this;
	};
})(jQuery);



/*
Modal overlay window handling
-----------------------------
Makes links call overlays with the linked page as content.
To activate just add `rel="niveOverlay"` as attribute to a link (a).

Uses the parents (the page containing the link) `#container` element to
position the overlay. The area outside gets a opacity of 70 % by default.

Example: ::

  <a href="http://cms.nive.co" rel="niveOverlay">Link</a>

*/
(function ($) {
      
    var _settings = {
        overlayOpacity: .85, // Use this value if not set in CSS or HTML
        id: 'modal',
        src: function (sender) {
            return jQuery(sender).attr('href');
        },
        fadeInSpeed: 0,
        fadeOutSpeed: 0,
        reloadOnClose: true,         // reload the parent on close
        closeOnClickOutside: true    // ask and close if clicked outside overlay
    }
      
    /********************************** 
    * DO NOT CUSTOMIZE BELOW THIS LINE 
    **********************************/  
    $.niveOverlay = function (id) {
        if(id) $(id+" a[rel^='niveOverlay']").attr("onClick", "$(this).modal().open(); return false;");
        else   $("a[rel^='niveOverlay']").attr("onClick", "$(this).modal().open(); return false;");
    }
    $.modal = function (options) {
        return _modal(this, options);
    }
    $.modal.open = function () {
        _modal.open();
    }
    $.modal.close = function () {
        _modal.close();
    }
    $.fn.modal = function (options) {
        return _modal(this, options);
    }
    _modal = function (sender, params) {
        this.options = {
            parent: null,
            overlayOpacity: null,
            id: null,
            content: null,
            modalClassName: null,
            imageClassName: null,
            closeClassName: null,
            overlayClassName: null,
            src: null
        }
        this.options = $.extend({}, options, _defaults);
        this.options = $.extend({}, options, _settings);
        this.options = $.extend({}, options, params);
        this.close = function (url) {
            jQuery('.' + options.modalClassName + ', .' + options.overlayClassName).fadeOut(_settings.fadeOutSpeed, function () { 
                      jQuery(this).unbind().remove(); 
                      if(!url) {
                      	if(options.reloadOnClose) location.reload(); 
                      } else {
                        location.href=url; 
                      } 
                   });
        }
        this.cancel = function () {
            jQuery('.' + options.modalClassName + ', .' + options.overlayClassName).fadeOut(_settings.fadeOutSpeed, function () { 
                      jQuery(this).unbind().remove(); });
        }
        this.open = function () {
            if (typeof options.src == 'function') {
                options.src = options.src(sender);
            } else {
                options.src = options.src || _defaults.src(sender);
            }
  
            var fileExt = /^.+\.((jpg)|(gif)|(jpeg)|(png)|(jpg))$/i;
            var contentHTML = '';
            if (fileExt.test(options.src)) {
                contentHTML = '<div class="' + options.imageClassName + '"><img src="' + options.src + '"/></div>';
            } else {
                contentHTML = '<iframe frameborder="0" allowtransparency="true" src="' + options.src + '"></iframe>';
            }
            options.content = options.content || contentHTML;
   
            if (jQuery('.' + options.modalClassName).length && jQuery('.' + options.overlayClassName).length) {
                jQuery('.' + options.modalClassName).html(options.content);
            } else {
                $overlay = jQuery((_isIE6()) ? '<iframe src="BLOCKED SCRIPT\'<html></html>\';" scrolling="no" frameborder="0" class="' + 
                                               options.overlayClassName + '"></iframe><div class="' + options.overlayClassName + '"></div>' : 
                                               '<div class="' + options.overlayClassName + '"></div>');
                $overlay.hide().appendTo(options.parent);
      
                $modal = jQuery('<div id="' + options.id + '" class="' + options.modalClassName + '" >' + options.content + '</div>');
                $modal.hide().appendTo(options.parent);
     
                $close = jQuery('<a id="' + options.closeClassName + '"></a>');
                $close.appendTo($modal);
      
                var overlayOpacity = _getOpacity($overlay.not('iframe')) || options.overlayOpacity;
                $overlay.fadeTo(0, 0).show().not('iframe').fadeTo(_settings.fadeInSpeed, overlayOpacity);
                $modal.fadeIn(_settings.fadeInSpeed);
      
                $close.click(function () { jQuery.modal().close(); });
                if(options.closeOnClickOutside)
                    $overlay.click(function () { if(!confirm("Close window?")) return; jQuery.modal().cancel(); });
            }
        }
        return this;
    }
    _isIE6 = function () {
        if (document.all && document.getElementById) {
            if (document.compatMode && !window.XMLHttpRequest) {
                return true;
            }
        }
        return false;
    }
    _getOpacity = function (sender) {
        $sender = jQuery(sender);
        opacity = $sender.css('opacity');
        filter = $sender.css('filter');
     
        if (filter.indexOf("opacity=") >= 0) {
            return parseFloat(filter.match(/opacity=([^)]*)/)[1]) / 100;
        }
        else if (opacity != '') {
            return opacity;
        }
        return '';
    }
    _defaults = {
        parent: '#container',
        overlayOpacity: 70,
        id: 'modal',
        content: null,
        modalClassName: 'modal-window',
        imageClassName: 'modal-image',
        closeClassName: 'close-window',
        overlayClassName: 'modal-overlay',
        src: function (sender) {
            return jQuery(sender).attr('href');
        }
    }
})(jQuery); 
 
 
/**
* jQuery Cookie plugin
*
* Copyright (c) 2010 Klaus Hartl (stilbuero.de)
* Dual licensed under the MIT and GPL licenses:
* http://www.opensource.org/licenses/mit-license.php
* http://www.gnu.org/licenses/gpl.html
*
*/
jQuery.cookie = function (key, value, options) {

    // key and at least value given, set cookie...
    if (arguments.length > 1 && String(value) !== "[object Object]") {
        options = jQuery.extend({}, options);

        if (value === null || value === undefined) {
            options.expires = -1;
        }

        if (typeof options.expires === 'number') {
            var days = options.expires, t = options.expires = new Date();
            t.setDate(t.getDate() + days);
        }

        value = String(value);

        return (document.cookie = [
            encodeURIComponent(key), '=',
            options.raw ? value : encodeURIComponent(value),
            options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
            options.path ? '; path=' + options.path : '',
            options.domain ? '; domain=' + options.domain : '',
            options.secure ? '; secure' : ''
        ].join(''));
    }

    // key and possibly options given, get cookie...
    options = value || {};
    var result, decode = options.raw ? function (s) { return s; } : decodeURIComponent;
    return (result = new RegExp('(?:^|; )' + encodeURIComponent(key) + '=([^;]*)').exec(document.cookie)) ? decode(result[1]) : null;
};

     