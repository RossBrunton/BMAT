"use strict";

window.bmat = (function() {
    var bmat = {};
    
    var _update = function() {
        // Clean first
        _clean();
        
        // Delete button
        $(".delete.button").on("click", function() {
            var post = {};
            post.csrfmiddlewaretoken = $("#csrf").html();
            post.bookmark = $(this).parents(".bookmark").data("id");
            
            $.post("/bookmarks/delete", post, function(e) {
                if(e.deleted !== null) {
                    $("[data-id="+e.deleted+"]").remove();
                }
            }, "json");
        });
        
        // Open/close button
        $(".expand.button").on("click", function() {
            if($(this).hasClass("open")) {
                $(this).parents(".bookmark").children(".bookmarkBody").slideUp();
                $(this).removeClass("open");
            }else{
                $(this).parents(".bookmark").children(".bookmarkBody").slideDown();
                $(this).addClass("open");
            }
        });
        
        // Tag Entry
        $(".tagEntry").on("input", function(e) {
            var input = this;
            if(e.target.value.length < 4) return;
            
            $.get("/tags/suggest/"+e.target.value, "", function(data) {
                var html = "";
                
                for(var i = 0; i < data.tags.length; i ++) {
                    html += "<option value='"+data.tags[i]+"'/>";
                }
                
                $(input).siblings("datalist").html(html);
            }, "json");
        });
        
        // Title editing
        $(".editTitle").on("click", function(e) {
            if(!$(this).hasClass("open")) {
                $(this).parents(".bookmark").find(".title.noedit").hide();
                $(this).parents(".bookmark").find(".title.edit").show();
                $(this).parents(".bookmark").find(".title.edit input[name=name]").val(
                    $(this).parents(".bookmark").find(".title.noedit a").text()
                );
                $(this).addClass("open");
            }else{
                $(this).parents(".bookmark").find(".title.noedit").show();
                $(this).parents(".bookmark").find(".title.edit").hide();
                $(this).removeClass("open");
            }
        });
        
        // Rename and tag forms
        $("form.tagForm, form.renameForm").on("submit", function(e) {
            e.preventDefault();
            var elem = this;
            
            $.post(this.getAttribute("action"), $(this).serialize(), function(data) {
                _replaceBookmark($(elem).parents(".bookmark").data("id"), true);
                
            }, "json");
        });
        
        // Form submit buttons
        $(".add.button, .rename.button").on("click", function(e) {
            $(this).parents("form").submit();
        });
        
        
    };
    
    var _clean = function() {
        $(".delete.button").off();
        $(".expand.button").off();
        $(".tagEntry").off();
        
        $(".add.button").off();
        $("form.tagForm").off();
        
        $(".rename.button").off();
        $("form.renameForm").off();
        
        $(".editTitle").off();
    };
    
    var _prependBookmark = function(id) {
        $.get("/bookmarks/"+id+"/html", function(e) {
            $("#bookmark-list").prepend(e);
            _update();
        }, "text");
    };
    
    var _replaceBookmark = function(id, expand) {
        $.get("/bookmarks/"+id+"/html", function(e) {
            $("[data-id="+id+"]").replaceWith(e);
            $("[data-id="+id+"] > .bookmarkBody").show();
            _update();
        }, "text");
    };
    
    var _ready = function() {
        // Bookmark adding
        $("#add-bookmark").on("submit", function(e) {
            e.preventDefault();
            $.post("/bookmarks/add", $(this).serialize(), function(e) {
                _prependBookmark(e.id);
                $(".addBookmark > input")[0].value = "";
            }, "json");
        });
    };
    
    $(_ready);
    $(_update);
    
    return bmat;
}());
