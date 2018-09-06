$(function() {
    var toggles = $(".search-toggle");
    var contents = $(".search-hidden-content");

	for(var i=0; i<toggles.length; i++){
        toggles.eq(i).bind("click", {index: i}, clickHandler);
    }

    function clickHandler(event) {
        var i= event.data.index;
        $(this).text(contents.eq(i).is(":hidden") ? "收起信息" : "更多信息");
        contents.eq(i).slideToggle();
    }

});
