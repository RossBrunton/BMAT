"use strict";

window.bmat = (function() {
    var bmat = {};
    
    var disabledForms = [];
    
    var undoCallback = null;
    
    var searchCount = 0;
    
    // Error handling
    var _error = function(message) {
        $("#error .errorText").html(message);
        $("#error").slideDown();
    }
    
    $(document).ajaxError(function(e, xhr, settings, error) {
        if("responseJSON" in xhr && "error" in xhr.responseJSON) {
            _error(xhr.responseJSON.error);
        }else{
            _error("ERROR: "+error);
        }
        
        _enableAllForms();
    });
    
    window.addEventListener("error", function(e) {
        _error(e.message);
    });
    
    
    // Function that finds the form this element is in, and submits it
    var _submitParent = function() {
        $(this).parents("form").submit();
        _disableForm(this);
    };
    
    // And a function that disables a form
    var _disableForm = function(e) {
        $(e).parents(".block").addClass("disabled");
        $(e).parents(".block").find("input, select").attr("disabled", "disabled");
        $(e).find("input, select").attr("disabled", "disabled");
        disabledForms.push(e);
    };
    
    // And to enable all of them again
    var _enableAllForms = function() {
        for(var i = 0; i < disabledForms.length; i ++) {
            var f = disabledForms[i];
            
            $(f).parents(".block").removeClass("disabled");
            $(f).parents(".block").find("input, select").removeAttr("disabled");
        }
        disabledForms = [];
    };
    
    // And the undo thing
    var _displayUndo = function(message, url, payload, callback) {
        $("#undo .undoText").html(message);
        $("#undo").slideDown();
        
        $("#undoForm [name=obj]").val(JSON.stringify(payload));
        $("#undoForm").attr("action", url);
        undoCallback = callback;
        
        $("#undoForm").find("input, select").removeAttr("disabled");
    };
    
    
    // Resets all the listeners, used when a document has been changed or initially loaded
    var _update = function() {
        // Remove all the old listeners
        _clean();
        
        // Delete button
        $(".block .delete.button").on("click", _submitParent);
        $(".deleteForm").on("submit", function(e) {
            e.preventDefault();
            
            var elem = $(this);
            var id = elem.parents(".block").attr("data-id");
            
            //if(!confirm("Are you sure you want to delete this?")) return;
            
            $.post(elem.attr("action"), elem.serialize(), function(data) {
                if(data.deleted !== null) {
                    elem.parents(".block").slideUp();
                    
                    _displayUndo("Object deleted", elem.attr("data-undo-url"), data.obj, function(dat) {
                        _replace(id, dat.type, false, true, dat.id);
                    });
                }
            });
        });
        
        
        // Inline untag button
        $(".inlineUntag.button").on("click", _submitParent);
        $(".inlineUntagForm").on("submit", function(e) {
            e.preventDefault();
            var elem = this;
            
            var bookmark = $(this).parents(".block").data("id");
            
            $.post(this.getAttribute("action"), $(this).serialize(), function(data) {
                _replace(bookmark, $(elem).parents(".block").data("taggable-type"), true);
            }, "json");
            
            _disableForm(this);
        });
        
        
        // Open/close button
        $(".expand.button").on("click", function() {
            if($(this).hasClass("open")) {
                $(this).parents(".block").children(".body").slideUp("fast");
                $(this).parents(".block").find(".inlineUntag").animate({"width":"0px"}, "fast");
                $(this).removeClass("open");
            }else{
                $(this).parents(".block").children(".body").slideDown("fast");
                $(this).parents(".block").find(".inlineUntag").animate({"width":"16px"}, "fast");
                $(this).addClass("open");
            }
        });
        
        // "Add tag" entry, for generating suggestions
        $(".tagEntry").on("input", function(e) {
            var input = this;
            
            // Don't bother with text less than 3 characters
            if(e.target.value.length < 3) return;
            
            // Get the suggestion list, and set the option elemnt to contain it
            $.get("/tags/suggest/"+e.target.value, "", function(data) {
                var html = "";
                
                for(var i = 0; i < data.tags.length; i ++) {
                    html += "<option value='"+data.tags[i]+"'/>";
                }
                
                $(input).siblings("datalist").html(html);
            }, "json");
        });
        
        // Title editing; hides the "real title" and replaces it with the text box, or the opposite
        $(".editTitle").on("click", function(e) {
            if(!$(this).hasClass("open")) {
                $(this).parents(".block").find(".noedit").hide();
                $(this).parents(".block").find(".edit").show();
                //$(this).parents(".block").find(".title.edit input[name=title]").val(
                //    $(this).parents(".block").find(".title.noedit a, .title.noedit").first().text()
                //);
                $(this).addClass("open");
            }else{
                $(this).parents(".block").find(".noedit").show();
                $(this).parents(".block").find(".edit").hide();
                $(this).removeClass("open");
            }
        });
        
        // Rename and tag forms, both do the same thing and both result in updating the block
        $(".rename.button").on("click", _submitParent);
        $("form.tagForm, form.renameForm").on("submit", function(e) {
            e.preventDefault();
            var elem = this;
            $(this).find("input[name=url]").val(
                $(elem).parents(".block").find(".body input[name=url]").val()
            );
            
            $.post(this.getAttribute("action"), $(this).serialize(), function(data) {
                _replace($(elem).parents(".block").data("id"), $(elem).parents(".block").data("taggable-type"), true);
            }, "json");
        });
        
        // And the submit button for the add tag button
        $(".addTag.button").on("click", function(e) {
            $(this).parents(".block").find(".tagForm").submit();
        });
    };
    
    // Removes all listeners
    var _clean = function() {
        $(".delete.button").off();
        $(".untag.button").off();
        $(".inlineUntag.button").off();
        $(".inlineUntagForm").off();
        $(".expand.button").off();
        $(".tagEntry").off();
        
        $(".addTag.button").off();
        $("form.tagForm").off();
        
        $(".rename.button").off();
        $("form.renameForm").off();
        
        $(".editTitle").off();
    };
    
    // Downloads a bookmark by an id and adds it to the list; used when adding a new one
    var _prependBookmark = function(id) {
        $.get("/bookmarks/"+id+"/html", function(e) {
            $("#bookmark-list").prepend(e);
            _update();
        }, "text");
    };
    
    
    // Given an id and a type, downloads a new version of the specific block and replaces them
    // If expand is true, then they are expanded as if the user had clicked the expand button
    var _replace = function(id, type, expand, slide, newid) {
        if(newid == undefined) newid = id;
        var url = "";
        if(type == "tag") url = "/tags/htmlBlock/" + newid;
        if(type == "bookmark") url = "/bookmarks/" + newid + "/html";
        
        $.get(url, function(e) {
            $(".block[data-id="+id+"]").replaceWith(e);
            if(expand) {
                $(".block[data-id="+id+"][data-taggable-type="+type+"] > .body").show();
                $(".block[data-id="+id+"][data-taggable-type="+type+"] .expand.button").addClass("open");
                $(".block[data-id="+id+"][data-taggable-type="+type+"] .inlineUntag")
                    .css("width", "16px").css("display", "inline-block");
                $(".block[data-id="+id+"][data-taggable-type="+type+"] input")[0].focus();
            }
            if(slide) {
                $(".block[data-id="+newid+"][data-taggable-type="+type+"]").css("display", "none");
                $(".block[data-id="+newid+"][data-taggable-type="+type+"]").slideDown();
            }
            _update();
        }, "text");
    };
    
    
    // Add the listeners on initial load
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
        $("#error .close.button").on("click", function(e) {
            $(this).parents("#error").slideUp();
        });
        
        // And handle undo
        $("#undo").on("submit", function(e) {
            e.preventDefault();
            
            var elem = $(this).find("form");
            
            $.post(elem.attr("action"), elem.serialize(), function(data) {
                undoCallback(data);
            }, "json");
            
            _disableForm(elem);
            
            $("#undo").slideUp();
        });
        
        $("#undo .close.button").on("click", function(e) {
            $(this).parents("#undo").slideUp();
        });
        
        // Search page
        $("#search-form input[name=q]").on("input", function(e) {
            var query = e.originalEvent.target.value;
            
            searchCount ++;
            var localSearchCount = searchCount;
            
            if("replaceState" in history) {
                history.replaceState({}, "", "?q="+encodeURIComponent(query).replace(/%20/gi, "+"));
            }
            
            $.get($("#search-form").attr("data-results"), $("#search-form").serialize(), function(results) {
                if(searchCount == localSearchCount) {
                    $("#search-results").html(results);
                    _update();
                }
            }, "html");
        });
    };
    
    // These two are ran on page load
    $(_ready);
    $(_update);
    
    return bmat;
}());
