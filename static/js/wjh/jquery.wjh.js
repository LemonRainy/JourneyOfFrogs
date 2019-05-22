let kunkun;
$(function () {
    //删除按钮所在表格的那行
    $('.btn-primary').click(function () {
        $(this).parent("td").parent("tr").remove();
    });


    //修改个人信息
    $("#change_personal_info").click(function () {
        var expert_name = $("#expert_name").val();
        var expert_tel = $("#expert_tel").val();
        var expert_intro = $("#expert_intro").val();

        $.ajax({
            type: "GET",
            url: "changeInfo",
            data: {
                'expert_name': expert_name,
                'expert_tel': expert_tel,
                'expert_intro': expert_intro,
            },
            success: function (data) {
                console.log(data)           // 这是json字符串
                // var data = JSON.parse(data) //JS 的json反序列化方法
                if (data.cool) {             //用点的方法取出键值
                    $("#disappare").show().delay(3000).hide(300);
                } else {
                    $("#disappare_2").show().delay(3000).hide(300);
                }

            },
            error: function (data) {
                $("#disappare_2").show().delay(3000).hide(300);
            }
        })
    });

    //修改密码
    $("#change_password").click(function () {
        var old_password = $("#old_password").val();
        var new_password = $("#new_password").val();
        var new_password_confirm = $("#new_password_confirm").val();
        $.ajax({
            type: "GET",
            url: "changePassword",
            data: {
                'old_password': old_password,
                'new_password': new_password,
                'new_password_confirm': new_password_confirm,
            },
            success: function (data) {
                console.log(data);       // 这是json字符串
                // var data = JSON.parse(data) //JS 的json反序列化方法

                $("#disappare_password").find('p').text(data.res_message);

                $("#disappare_password").show().delay(3000).hide(300);

            },
            error: function (data) {
                $("#disappare_password").find('p').text("哦呦，发生了不可描述的错误...");
                $("#disappare_password").show().delay(3000).hide(300);
            }
        })
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