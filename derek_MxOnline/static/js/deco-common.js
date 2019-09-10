//顶部个人中心下拉框
// 鼠标hover时显示/隐藏
$('.header .personal').hover(function(){
    $(".header .userdetail").stop(true).show();
}, function(){
    $('.header .userdetail').stop(true).hide();
});