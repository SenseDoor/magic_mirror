<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>魔镜控制器</title>
    <link href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <script src="http://code.jquery.com/jquery.js"></script>
    
    

    <style type="text/css">

        #up {
            margin-left: 120px;
            margin-bottom: 10px;
        }
        #down {
            margin-top: 20px;
            margin-left: 120px;
        }
        #stop {
            margin-top: 10px;
            margin-left: 10px;
        }       
        #left {
            margin-top: 10px;
            margin-left: 10px;
        }
        #right {
            margin-top: 10px;
            margin-left: 10px;
        }
    </style>

    <script>
        $(function(){
            $("button").click(function(){
                cmd="{cmd:"+this.id+"}"
                //alert(cmd)
                $.post("/cmd",this.id,function(data,status){
                });
            });

        });

    </script>
</head>
<body>
    <div id="container" class="container" >
        <div>
            <button id="up" class="btn btn-lg btn-primary glyphicon  glyphicon-ok-sign" style="font-size: 60px"></button>
        </div>
        <div>
            <button id='left' class="btn btn-lg btn-primary glyphicon glyphicon-camera" style="font-size: 60px"></button>
            <button id='stop' class="btn btn-lg btn-primary glyphicon glyphicon-off" style="font-size: 60px"></button>
            <button id='right' class="btn btn-lg btn-primary glyphicon  glyphicon-calendar" style="font-size: 60px"></button>
        </div>
        <div>
            <button id='down' class="btn btn-lg btn-primary glyphicon glyphicon-phone" style="font-size: 60px"></button>
        </div>

    </div>
    <div id="memory" style="clear:both;text-align:center;">
        <p>请输入备忘录</p>
        <form action='/new' method="GET">
            
            <textarea type="text" name="task" cols="50" rows="6"></textarea>
            <input type="submit" name="save" value="提交">
        </form>
    </div>

<script src="//cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
</body>
</html>
