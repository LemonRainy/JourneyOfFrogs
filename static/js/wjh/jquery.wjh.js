let kunkun;
$(function () {
    //删除按钮所在表格的那行
    $('.btn-primary').click(function () {
        $(this).parent("td").parent("tr").remove();
    });

    //显示 保存成功
    $("#change_personal_info").click(function () {
        $("#disappare").show().delay(3000).hide(300);
    });

    //----------------- 恶搞 可忽略--------------------------
    // kunkun = 0;
    // $(".wjh").css("background-image", "url(" + "\'/static/images/cxk.jpg\'" + ")");
    // $("h2.mb-3.bread").text("觉得不对？蔡徐坤让你敲回车试试？");
    // $(document).keydown(function (event) {
    //     if (event.keyCode === 13) {
    //         if (kunkun === 0) {
    //             $(".wjh").css("background-image", "url(" + "\'/static/images/wjh.jpg\'" + ")");
    //             $("h2.mb-3.bread").text("还觉得不对？再敲回车试试？");
    //             kunkun = 1;
    //         } else if (kunkun === 1) {
    //             $(".wjh").css("background-image", "url(" + "\'/static/images/bg_2.jpg\'" + ")");
    //             $("h2.mb-3.bread").remove();
    //             kunkun = 2;
    //         }
    //     }
    // });


});