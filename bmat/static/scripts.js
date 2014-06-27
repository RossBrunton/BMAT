"use strict";

window.bmat = (function() {
    var bmat = {};
    
    var _update = function() {
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
    };
    
    var _prependBookmark = function(id) {
        $.get("/bookmarks/"+id+"/html", function(e) {
            $("#bookmark-list").prepend(e);
        }, "text");
    };
    
    var _ready = function() {
        // Bookmark adding
        $("#add-bookmark").on("submit", function(e) {
            e.preventDefault();
            $.post("/bookmarks/add", $(this).serialize(), function(e) {
                _prependBookmark(e.id);
            }, "json");
        });
    };
    
    $(_ready);
    $(_update);
    
    return bmat;
}());
