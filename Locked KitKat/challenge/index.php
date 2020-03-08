<?php
require 'recaptcha.php';

if (!empty($_POST['pattern'])) {
    if (reCAPTCHA()) {
        if ($_POST['pattern'] === '321564') {
            $flag = "zer0pts{n0th1ng_1s_m0r3_pr4ct1c4l_th4n_brut3_f0rc1ng}";
        } else {
            $error = "Unlock Failed";
        }
    } else {
        $error = "Captcha Error";
    }
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Locked KitKat</title>
        <style media="screen">
         * {
             box-sizing: border-box;
         }

         html, body {
             padding: 0;
             margin: 0;
             height: 100vh;
             max-height: 100vh;
         }

         body {
             font-family: Consolas, 'Courier New', Courier, Monaco, monospace;
         }

         .center {
             margin-right: auto;
             margin-left: auto;
             text-align: center;
         }

         button {
             background: #3498db;
             height: 64px;
             width: 180px;
             padding: 4px 0;
             border-radius: 8px;
             border: 0 solid;
             font-size: 24px;
             color: white;
             cursor: pointer;
         }

         .container {
             margin: auto;
             height: 50%;
         }

         h1 {
             text-align: center;
             margin-top: 2vh;
             text-align: center;
             font-size: 6vh;
         }

         #lock {
             width: 100%;
             height: calc(100% - 8vh);
             min-height: 120px;
         }

         .error {
             color: red;
         }
         .success {
             color: green;
         }
        </style>
        
        <link rel="stylesheet" href="assets/patternlock.css">
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.slim.min.js" charset="utf-8"></script>
        <script src="https://www.google.com/recaptcha/api.js"></script>
        <script src="assets/patternlock.js" charset="utf-8"></script>
    </head>

    <body>
        <div class="container">
            <h1>Locked KitKat</h1>
            <div class="error center"><?php if (isset($error)) { print($error); } ?></div>
            <div class="success center"><?php if (isset($flag)) { print($flag); } ?></div>
            <svg class="patternlock" id="lock" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <g class="lock-actives"></g>
                <g class="lock-lines"></g>
                <g class="lock-dots">
                    <circle cx="20" cy="20" r="2"/>
                    <circle cx="50" cy="20" r="2"/>
                    <circle cx="80" cy="20" r="2"/>
                    
                    <circle cx="20" cy="50" r="2"/>
                    <circle cx="50" cy="50" r="2"/>
                    <circle cx="80" cy="50" r="2"/>
                    
                    <circle cx="20" cy="80" r="2"/>
                    <circle cx="50" cy="80" r="2"/>
                    <circle cx="80" cy="80" r="2"/>
                </g>
            </svg>
        </div>
        
        <form action="/" method="POST" class="center" id="unlock">
            <div class="center" style="width: 324px; padding: 2vh;">
        	      <div class="g-recaptcha" data-sitekey="6LcZ1r0UAAAAAJcyneDQonYeGx_ulXuSXpKRux_R"></div>
            </div>
            <button type="submit">Unlock</button>
        </form>

        <script type="text/javascript">
         var e = document.getElementById('lock')
         var p = new PatternLock(e, {
             onPattern: function() {
                 this.success();
             }
         });

         $('#unlock').submit(function() {
             var params = [{
                 name: 'pattern', value: p.getPattern()
             }];
             $(this).append($.map(params, function(param) {
                 return $('<input>', {
                     type: 'hidden',
                     name: param.name,
                     value: param.value
                 })
             }));
             return true;
         });
        </script>
    </body>
</html>
