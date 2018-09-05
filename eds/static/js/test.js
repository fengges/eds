$(function() {
    var toggles = $(".search-toggle");
    var contents = $(".search-hidden-content");
    var toggle = toggles.eq(0);
    alert(toggles.length);

//	toggle.click(function(){
//      content = contents.eq(0);
//            alert(content.innerHTML);
//            content.slideToggle();
//    });
	for(var i=0; i<toggles.length; i++){
        toggles.eq(i).click(function() {
//            $(this).text(contents.eq(i).is(":hidden") ? "收起" : "展开");
            contents.eq(i).slideToggle();
        });
    }
});
