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
            
            if($(this).parents(".bookmark").length) {
                // Deleting a bookmark
                post.bookmark = $(this).parents(".bookmark").data("id");
                
                $.post("/bookmarks/delete", post, function(e) {
                    if(e.deleted !== null) {
                        $(".bookmark[data-id="+e.deleted+"]").slideUp().remove();
                    }
                }, "json");
            }else{
                // Deleting a tag
                post.tag = $(this).parents(".tagBlock").data("id");
                
                $.post("/tags/delete", post, function(e) {
                    if(e.deleted !== null) {
                        $(".tagBlock[data-id="+e.deleted+"]").slideUp().remove();
                    }
                }, "json");
            }
        });
        
        // Open/close button
        $(".expand.button").on("click", function() {
            if($(this).hasClass("open")) {
                $(this).parents(".bookmark").children(".bookmarkBody").slideUp("fast");
                $(this).parents(".tagBlock").children(".tagBlockBody").slideUp("fast");
                $(this).removeClass("open");
            }else{
                $(this).parents(".bookmark").children(".bookmarkBody").slideDown("fast");
                $(this).parents(".tagBlock").children(".tagBlockBody").slideDown("fast");
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
                $(this).parents(".bookmark, .tagBlock").find(".title.noedit").hide();
                $(this).parents(".bookmark, .tagBlock").find(".title.edit").show();
                $(this).parents(".bookmark, .tagBlock").find(".title.edit input[name=name]").val(
                    $(this).parents(".bookmark, .tagBlock").find(".title.noedit a, .title.noedit").first().text()
                );
                $(this).addClass("open");
            }else{
                $(this).parents(".bookmark, .tagBlock").find(".title.noedit").show();
                $(this).parents(".bookmark, .tagBlock").find(".title.edit").hide();
                $(this).removeClass("open");
            }
        });
        
        // Rename and tag forms
        $("form.tagForm, form.renameForm").on("submit", function(e) {
            e.preventDefault();
            var elem = this;
            
            $.post(this.getAttribute("action"), $(this).serialize(), function(data) {
                if("bookmark" in data) _replaceBookmark($(elem).parents(".bookmark").data("id"), true);
                if("tag" in data) _replaceTagBlock($(elem).parents(".tagBlock").data("slug"), true);
            }, "json");
        });
        
        // Form submit buttons
        $(".rename.button").on("click", function(e) {
            $(this).parents("form").submit();
        });
        
        $(".addTag.button").on("click", function(e) {
            $(this).parents(".tagBlock, .bookmark").find(".tagForm").submit();
        });
    };
    
    var _clean = function() {
        $(".delete.button").off();
        $(".expand.button").off();
        $(".tagEntry").off();
        
        $(".addTag.button").off();
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
            $(".bookmark[data-id="+id+"]").replaceWith(e);
            if(expand) $(".bookmark[data-id="+id+"] > .bookmarkBody").show();
            _update();
        }, "text");
    };
    
    var _replaceTagBlock = function(slug, expand) {
        $.get("/tags/htmlBlock/"+slug, function(e) {
            $(".tagBlock[data-slug="+slug+"]").replaceWith(e);
            if(expand) $(".tagBlock[data-slug="+slug+"] > .tagBlockBody").show();
            _update();
        }, "text");
    };
    
    
    var _ready = function() {
        // Bookmark adding
        $("#add-bookmark").on("submit", function(e) {
            e.preventDefault();
            $.post("/bookmarks/add", $(this).serialize(), function(e) {
                _prependBookmark(e.id);
                $("#add-bookmark > input[name=url]")[0].value = "";
            }, "json");
        });
    };
    
    $(_ready);
    $(_update);
    
    return bmat;
}());
