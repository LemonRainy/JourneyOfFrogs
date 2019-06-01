let kunkun;
$(function () {
    //接受
    $("button[name='accept']").click(function () {
        //获取所在列的订单编号
        var t = $(this);
        var order_id = $(this).parent("td").parent("tr").children().eq(0).text();
        console.log("接受订单编号：" + order_id);
        $.ajax({
            type: "GET",
            url: "acceptOrder",
            data: {
                'order_id': order_id,
            },
            success: function (data) {
                if (data.cool) {
                    t.parent("td").find("button[name='accept']").hide();
                    t.parent("td").find("button[name='refuse']").hide();

                    t.parent("td").find("button[name='end']").fadeIn(2000,function(){});
                    t.parent("td").find("button[name='cancel']").fadeIn(2000,function(){});



                } else {
                    alert("接受订单失败!")
                }

            },
            error: function (data) {
                alert("接受订单失败!")

            }
        })
    });

    //拒绝
    $("button[name='refuse']").click(function () {
        //获取所在列的订单编号
        var t = $(this);
        var order_id = $(this).parent("td").parent("tr").children().eq(0).text();
        console.log("拒绝订单编号：" + order_id);
        $.ajax({
            type: "GET",
            url: "refuseOrder",
            data: {
                'order_id': order_id,
            },
            success: function (data) {
                if (data.cool) {
                    t.parent("td").parent("tr").remove();

                } else {
                    alert("拒绝订单失败!")
                }

            },
            error: function (data) {
                alert("拒绝订单失败!")

            }
        })
    });

    //结束
    $("button[name='end']").click(function () {
        //获取所在列的订单编号
        var t = $(this);
        var order_id = $(this).parent("td").parent("tr").children().eq(0).text();
        console.log("结束订单编号：" + order_id);
        $.ajax({
            type: "GET",
            url: "endOrder",
            data: {
                'order_id': order_id,
            },
            success: function (data) {
                if (data.cool) {
                    t.parent("td").parent("tr").remove();

                } else {
                    alert("结束订单失败!")
                }

            },
            error: function (data) {
                alert("结束订单失败!")

            }
        })
    });

    //取消
    $("button[name='cancel']").click(function () {
        //获取所在列的订单编号
        var t = $(this);
        var order_id = $(this).parent("td").parent("tr").children().eq(0).text();
        console.log("取消订单编号：" + order_id);
        $.ajax({
            type: "GET",
            url: "cancelOrder",
            data: {
                'order_id': order_id,
            },
            success: function (data) {
                if (data.cool) {
                    t.parent("td").parent("tr").remove();

                } else {
                    alert("取消订单失败!")
                }

            },
            error: function (data) {
                alert("取消订单失败!")

            }
        })
    });


    //修改个人信息
    $("#change_personal_info").click(function () {
        var expert_name = $("#expert_name").val();
        var expert_tel = $("#expert_tel").val();
        var expert_intro = $("#expert_intro").val();
        var expert_gender = $("#expert_gender").val();
        var expert_seniority = $("#expert_seniority").val();
        var expert_company = $("#expert_company").val();
        var expert_tag = $("#expert_tag").val();


        $.ajax({
            type: "GET",
            url: "changeInfo",
            data: {
                'expert_name': expert_name,
                'expert_tel': expert_tel,
                'expert_intro': expert_intro,
                'expert_gender': expert_gender,
                'expert_seniority': expert_seniority,
                'expert_company': expert_company,
                'expert_tag': expert_tag,
            },
            success: function (data) {
                // data:
                //     cool: 代表修改是否成功

                // var data = JSON.parse(data) //JS 的json反序列化方法
                if (data.cool) {             //用点的方法取出键值
                    $("#disappare_info").find('p').css("color", "green");
                    $("#disappare_info").find('p').text("修改成功!");
                    $("#disappare_info").show().delay(3000).hide(300);
                } else {
                    $("#disappare_info").find('p').css("color", "red");
                    $("#disappare_info").find('p').text("修改失败!");
                    $("#disappare_info").show().delay(3000).hide(300);
                }

            },
            error: function (data) {
                $("#disappare_info").find('p').css("color", "red");
                $("#disappare_info").find('p').text("哦呦，发生了不可描述的错误...");
                $("#disappare_info").show().delay(3000).hide(300);
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
                // data:
                //     cool: 代表修改是否成功
                //     res_message: 返回的信息，"修改成功"，"旧密码错误"， "两次新密码不一致"

                if (data.cool) {
                    $("#disappare_password").find('p').css("color", "green");
                } else {
                    $("#disappare_password").find('p').css("color", "red");
                }
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