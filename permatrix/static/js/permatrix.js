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