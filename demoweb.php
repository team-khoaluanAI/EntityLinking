<?php
    $result="";
    $output='';
    $str='';
    if(isset($_POST["textinput"]))
    {
        $str =$_POST["textinput"];
        // $command = escapeshellcmd('entity.py'.$str);
        // $output = shell_exec($command);
        //$ouput=exec("/usr/custom/main.py");
        $output = exec("python Main.py $str");
        // echo $output;
        $result=$output;
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
    <title>LIÊN KẾT THỰC THỂ TRONG VĂN BẢN TIẾNG VIỆT
    </title>
    <style type="text/css">
        #box {
        width: 500px;
        height: 318px;
        margin: 0 auto;
        overflow: auto;
        border: 1px solid;
        border-color: #C0C0C0; 
        padding: 2px;
        text-align: justify;
        background: transparent;
        }
    </style>

</head>
<body>

    <div class="p-2 mb-2 bg-info text-white">
        <center><h2 class="text-warning">Nhận Diện Thực Thể Đặt Tên Trong Văn Bản Tiếng Việt</h2></center>
    </div>
    <hr width="30%" size="10px" align="center"/>
    <div class="demo-area" style="max-width: 1000px; margin: auto;">
        <div class="row demo-ocr justify-content-lg-between">
            <div class="col-md-6 demo-ocr-col mb-4 mb-md-0">
                <div><h5>Nhập đoạn văn bản đầu vào</h5></div> 
                <form method="post">
                <textarea rows="13" cols="50" maxlength="3110" name= "textinput" placeholder="Bắt đầu nhập tại đây" style="width: 100%; resize: none;"><?php echo $str?></textarea> 
                <div>
                    <button class="btn btn-info btn-lg">Phân tích</button>
                </div>
                </form>
            </div> 
            <div class="col-md-6 demo-ocr-col">
                <div><h5>Kết quả phân tích</h5></div> 
                <div id='box'><?php echo $result?></div>
            </div>
        </div>
    </div>

</body>
</html>