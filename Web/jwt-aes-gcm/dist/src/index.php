<?php
require "utils/JWT.php";

$jwt = new JWT(getenv("SECRET"));
if (!isset($_COOKIE["jwt"])){
    $token = $jwt->encode(array('role'=>'guest'));
    $_COOKIE["jwt"] = $token;
    setcookie("jwt", $_COOKIE['jwt']);
}

$session = $jwt->decode($_COOKIE["jwt"]);

if ($session["role"] === "admin"){
    echo getenv("FLAG");
}else{
    print_r($session);
    echo "Hello World";
}
