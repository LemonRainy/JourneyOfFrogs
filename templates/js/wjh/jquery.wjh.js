let i;
$(function () {
    //删除按钮所在表格的那行
    $('.btn-primary').click(function () {
        $(this).parent("td").parent("tr").remove();
    });

    //显示 保存成功
    $("#change_personal_info").click(function () {
        $("#disappare").show().delay(3000).hide(300);
    });

    //恶搞
    i = 0;
    $(document).keydown(function (event) {
        if (event.keyCode === 13) {

            if (i === 0) {
                $(".wjh").css("background-image", "url(" + "\'images/wjh.jpg\'" + ")");
                $("h2.mb-3.bread").text("还觉得不对？再敲回车试试？");
                i = 1;
            } else if (i === 1) {
                $(".wjh").css("background-image", "url(" + "\'images/bg_2.jpg\'" + ")");
                $("h2.mb-3.bread").remove();
                i = 2;
            }


        }
    });


});