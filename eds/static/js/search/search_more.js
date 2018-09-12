$(function() {

    //点击加载更多

    var toggles = $(".search-toggle");
    var contents = $(".search-hidden-content");

	for(var i=0; i<toggles.length; i++){
        toggles.eq(i).bind("click", {index: i}, clickHandler);
    }

    function clickHandler(event) {
        var i= event.data.index;
        $(this).html(contents.eq(i).is(":hidden") ? "收起信息<i class='glyphicon glyphicon-chevron-up'></i>" : "更多信息<i class='glyphicon glyphicon-chevron-down'></i>");

        contents.eq(i).slideToggle();
    }

    //按钮“更多信息”隐藏
    var persons = $(".search-person>li");
    for(var i=0; i<persons.length; i++){
        persons.eq(i).hover(function(){
            $(this).find(".search-toggle").css('visibility', 'visible')
        }, function(){
            $(this).find(".search-toggle").css('visibility', 'hidden')
        });
    }

    //关键词

    var reg = /test\/(.*)/
    $("#keyword").text(decodeURI(decodeURI(reg.exec(document.URL)[1])));

    //人数
    $("#person_count").text(persons.length)
});
