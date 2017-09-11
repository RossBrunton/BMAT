"use strict";

window.bmatFn = function() {
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
        $("#undo").stop().slideDown();
        
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
                    elem.parents(".block").stop().slideUp();
                    
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
            
            var taggable = $(this).parents(".block").data("id");
            
            $.post(this.getAttribute("action"), $(this).serialize(), function(data) {
                _replace(taggable, $(elem).parents(".block").data("taggable-type"), false);
            }, "json");
            
            _disableForm(this);
        });
        
        
        // Open/close button
        var _expand = function() {
            if($(this).hasClass("open")) {
                $(this).parents(".block").children(".body").stop().slideUp("fast");
                $(this).parents(".block").find(".inlineUntag").stop().animate({"width":"0px"}, "fast");
                $(this).removeClass("open");
                _hideEditing($(this).parents(".block"));
            }else{
                $(this).parents(".block").children(".body").stop().slideDown("fast");
                $(this).parents(".block").find(".inlineUntag").stop().animate({"width":"16px"}, "fast");
                $(this).addClass("open");
            }
        };
        $(".expand.button").on("click", _expand);
        $(".head").on("dblclick", _expand);
        
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
        var _showEditing = function(e) {
            $(e).find(".noedit").hide();
            $(e).find(".edit").show();
            $(e).addClass("editing");
        };
        
        var _hideEditing = function(e) {
            $(e).find(".noedit").show();
            $(e).find(".edit").hide();
            $(e).removeClass("editing");
        };
        
        $(".editTitle, .editPattern").on("click", function(e) {
            var block = $(this).parents(".block");
            
            if(!block.hasClass("editing")) {
                _showEditing(block);
            }else{
                _hideEditing(block);
            }
        });
        
        // Rename and tag forms, both do the same thing and both result in updating the block
        $(".rename.button").on("click", function() {
            var form = $(this).parents(".block").find(".renameForm");
            form.submit();
            _disableForm(form);
        });
        $(".setPattern.button").on("click", function() {
            var form = $(this).parents(".block").find(".setPatternForm");
            form.submit();
            _disableForm(form);
        });
        $("form.tagForm, form.renameForm, form.setPatternForm").on("submit", function(e) {
            e.preventDefault();
            var elem = this;
            
            $(this).find("input[name=url]").val(
                $(elem).parents(".block").find(".body input[name=url]").val()
            );
            
            var focus = $(this).hasClass("tagForm");
            
            $.post(this.getAttribute("action"), $(this).serialize(), function(data) {
                _replace($(elem).parents(".block").data("id"), $(elem).parents(".block").data("taggable-type"), 
                function(node) {
                    if(focus) {
                        $(node).find("input[name=name]").focus();
                    }
                }, false, data.obj.id);
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
        
        $(".setPattern.button").off();
        $("form.setPatternForm").off();
        
        $(".editTitle").off();
    };
    
    // Downloads a bookmark by an id and adds it to the list; used when adding a new one
    var _prependBookmark = function(id) {
        $.get("/bookmarks/"+id+"/html", function(e) {
            $("#bookmark-list").prepend(e);
            _update();
        }, "text");
    };
    
    // And ditto for autotags
    var _prependAutotag = function(id) {
        $.get("/autotags/"+id+"/html", function(e) {
            $("#autotag-list").prepend(e);
            _update();
        }, "text");
    };
    
    
    // Given an id and a type, downloads a new version of the specific block and replaces them
    var _replace = function(id, type, callback, slide, newid) {
        if(newid == undefined) newid = id;
        var url = "";
        if(type == "tag") url = "/tags/htmlBlock/" + newid;
        if(type == "bookmark") url = "/bookmarks/" + newid + "/html";
        if(type == "autotag") url = "/autotags/" + newid + "/html";
        
        var displayMultiCheck = $(".block[data-id="+id+"] .multiTagCheck").css("width") == "16px";
        var multiChecked = $(".block[data-id="+id+"] .multiTagCheck:checked").length > 0;
        var expand = $(".block[data-id="+id+"] .expand.open").length > 0;
        
        $.get(url, function(e) {
            $(".block[data-id="+id+"]").replaceWith(e);
            if(expand) {
                $(".block[data-id="+id+"][data-taggable-type="+type+"] > .body").show();
                $(".block[data-id="+id+"][data-taggable-type="+type+"] .expand.button").addClass("open");
                $(".block[data-id="+id+"][data-taggable-type="+type+"] .inlineUntag")
                    .css("width", "16px").css("display", "inline-block");
                if($(".block[data-id="+id+"][data-taggable-type="+type+"] input")[0])
                    $(".block[data-id="+id+"][data-taggable-type="+type+"] input")[0].focus();
            }
            if(slide) {
                $(".block[data-id="+newid+"][data-taggable-type="+type+"]").css("display", "none");
                $(".block[data-id="+newid+"][data-taggable-type="+type+"]").stop().slideDown();
            }
            
            if(displayMultiCheck) {
                $(".block[data-id="+newid+"] .multiTagCheck").show()
                    .css("width", "16px").css("margin-left", "5px").css("margin-right", "5px");
            }
            if(multiChecked) {
                $(".block[data-id="+newid+"] .multiTagCheck").prop("checked", true);
            }
            _update();
            if(callback) callback($(".block[data-id="+newid+"][data-taggable-type="+type+"]"));
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
        
        // Autotag pattern adding
        $("#add-pattern").on("submit", function(e) {
            e.preventDefault();
            $.post("/autotags/add", $(this).serialize(), function(e) {
                _prependAutotag(e.id);
                $("#add-pattern > input[name=pattern]")[0].value = "";
            }, "json");
        });
        
        // Error closing
        $("#error .close.button").on("click", function(e) {
            $(this).parents("#error").stop().slideUp();
        });
        
        // Multitag expand
        $(".multiTag.button").on("click", function(e) {
            if($(this).hasClass("open")) {
                $(this).removeClass("open");
                $(".multiTagCheck").stop().animate({
                    width:"0px", minWidth:"0px", marginRight:"0px", marginLeft:"0px"}, 350, "swing",
                    function() {
                        $(".multiTagCheck").hide();
                    }
                );
                $(".multiTagBox").stop().slideUp();
            }else{
                $(this).addClass("open");
                $(".multiTagCheck").stop().show().animate({width:"16px", minWidth:"16px", marginRight:"5px", marginLeft:"5px"},
                    350
                );
                $(".multiTagBox").stop().slideDown();
            }
        });
        
        // "Select all" button for multitag
        $(".multiTagAll.button").on("click", function(e) {
            if($(".multiTagCheck:checked").length == $(".multiTagCheck").length) {
                // All checked
                $(".multiTagCheck").prop("checked", false);
            }else{
                $(".multiTagCheck").prop("checked", true);
            }
        });
        
        // When the multitag form is submitted
        $(".multiTagForm").on("submit", function(e) {
            e.preventDefault();
            var tag = $(this).find("[name=name]").val();
            var colour = $(this).find("[name=colour]").val();
            
            $(".multiTagCheck:checked").parents(".block").find(".tagForm").each(function(i, node) {
                $(node).find("[name=name]").val(tag);
                $(node).find("[name=colour]").val(colour);
                $(node).submit();
            });
        });
        
        // And handle undo
        $("#undo").on("submit", function(e) {
            e.preventDefault();
            
            var elem = $(this).find("form");
            
            $.post(elem.attr("action"), elem.serialize(), function(data) {
                undoCallback(data);
            }, "json");
            
            _disableForm(elem);
            
            $("#undo").stop().slideUp();
        });
        
        $("#undo .close.button").on("click", function(e) {
            $(this).parents("#undo").stop().slideUp();
        });
        
        // And handle the pinning form
        $("#pinForm").on("submit", function(e) {
            e.preventDefault();
            
            var elem = $(this);
            
            $.post(elem.attr("action"), elem.serialize(), function(data) {
                document.location.reload();
            }, "json");
            
            _disableForm(elem);
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
};

window.bmatCheckReady = function() {
    if("$" in window) {
        window.bmat = window.bmatFn();
    }else{
        setTimeout(window.bmatCheckReady, 100);
    }
}

bmatCheckReady();
