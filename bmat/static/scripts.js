"use strict";

window.bmat = (function() {
    var bmat = {};
    
    var _error = function(message) {
        $("#error .errorText").html(message);
        $("#error").slideDown();
    }
    
    window.addEventListener("error", function(e) {
        _error(e.message);
    });
    
    $(document).ajaxError(function(e, xhr, settings, error) {
        if("responseJSON" in xhr && "error" in xhr.responseJSON) {
            _error(xhr.responseJSON.error);
        }else{
            _error("ERROR: "+error);
        }
    });
    
    var _update = function() {
        // Clean first
        _clean();
        
        // Delete button
        $(".bookmark .delete.button, .tagBlock .delete.button").on("click", function() {
            var post = {};
            post.csrfmiddlewaretoken = $("#csrf").html();
            
            if(!confirm("WHOA! Are you sure!")) return;
            
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
        
        // Untag button
        $(".untag.button").on("click", function() {
            var elem = this;
            
            var post = {};
            post.csrfmiddlewaretoken = $("#csrf").html();
            
            post.bookmark = $(this).parents(".bookmark").data("id");
            post.tag = $(this).data("slug");
            
            $.post("/bookmarks/"+post.bookmark+"/untag", post, function(e) {
                $(elem).parents(".bookmark").remove();
            }, "json");
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
                if("tag" in data) _replaceTagBlock($(elem).parents(".tagBlock").data("slug"), data.tag.slug, true);
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
        $(".bookmark .delete.button, .tagBlock .delete.button").off();
        $(".untag.button").off();
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
            if(expand) {
                $(".bookmark[data-id="+id+"] > .bookmarkBody").show();
                $(".bookmark[data-id="+id+"] .expand.button").addClass("open");
            }
            _update();
        }, "text");
    };
    
    var _replaceTagBlock = function(oldSlug, newSlug, expand) {
        $.get("/tags/htmlBlock/"+newSlug, function(e) {
            $(".tagBlock[data-slug="+oldSlug+"]").replaceWith(e);
            if(expand) {
                $(".tagBlock[data-slug="+newSlug+"] > .tagBlockBody").show();
                $(".tagBlock[data-slug="+newSlug+"] .expand.button").addClass("open");
            }
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
        
        // Error closing
        $("#error .delete.button").on("click", function(e) {
            $(this).parents("#error").slideUp();
        });
    };
    
    $(_ready);
    $(_update);
    
    return bmat;
}());
