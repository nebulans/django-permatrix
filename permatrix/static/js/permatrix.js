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

$(document).on("click", ".permission-cell", function(){
    var t = $(this);
    var actions_container = $("#pending-actions");
    var action_elem = $("<li>");
    action_elem.data("permission", t.data("permission_id"));
    action_elem.data("group", t.data("group_id"));
    if (t.hasClass("perm_yes")) {
        action_elem.text("Remove permission " + t.data("permission_name") + " from group " + t.data("group_name"));
        action_elem.data("action", "remove");
        t.removeClass("perm_yes");
        t.addClass("perm_remove");
    } else {
        action_elem.text("Add permission " + t.data("permission_name") + " to group " + t.data("group_name"))
        action_elem.data("action", "add");
        t.addClass("perm_add");
    }
    actions_container.append(action_elem)
});

$(document).on("click", ".submit-perms", function(){
    // Collect data from pending changes list
    var perm_changes = [];
    $("#pending-actions li").each(function(){
        var t = $(this);
        perm_changes.push({
            group: t.data("group"),
            permission: t.data("permission"),
            action: t.data("action")
        })
    });
    // Make AJAX request
    $.ajax({
        method: "POST",
        data: {data: JSON.stringify(perm_changes)},
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    }).done(function(){
        // Permission updates successful
        // Clear pending updates list
        $("#pending-actions").html("");
        // Remove all perm_remove classes
        $(".perm_remove").removeClass("perm_remove");
        // Remove all perm_add classes and replace with perm_yes
        $(".perm_add").removeClass("perm_add").addClass("perm_yes");
    }).fail(function(){
        $(".actions").append("<p>An error occured</p>")
    })
});