<?php

$cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg%3D";
$cookie = urldecode($cookie);
$cookie = base64_decode($cookie);
function xor_encrypt($in)
{
    $key = 'eDWo';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for ($i = 0; $i < strlen($text); $i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

$new_cookie_array = array("showpassword" => "yes", "bgcolor" => "#f0f0aa");
echo base64_encode(xor_encrypt(json_encode($new_cookie_array)));

?>