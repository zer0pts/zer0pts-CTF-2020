<?php
function reCAPTCHA() {
    if (empty($_REQUEST['g-recaptcha-response'])) {
        return false;
    }
    
    $url = 'https://www.google.com/recaptcha/api/siteverify';
    $data = array(
        'secret' => '6LcZ1r0UAAAAAFDFRgDIDZgJguc2YYGjXPLDX1cT',
        'response' => $_REQUEST['g-recaptcha-response'],
        'remoteip' => $_SERVER['REMOTE_ADDR'],
    );
    $url .= '?' . http_build_query($data);
    $header = Array(
        'Content-Type: application/x-www-form-urlencoded',
    );
    $options = array('http' =>
        array(
            'method' => 'GET',
            'header'  => implode("\r\n", $header),
            'ignore_errors' => true
        )
    );
    $apiResponse = file_get_contents($url, false, stream_context_create($options));
    
    $jsonData = json_decode($apiResponse, true);
    if($jsonData['success'] === true){
        return true;
    } else {
        return false;
    }
}
?>
