<?php
$allowedUserAgent = 'TRY USING BRAVE BROWSER'; // User-Agent yang diizinkan
$validUsername = 'brave'; // Nama pengguna yang diharapkan
$validPassword = 'browser'; // Kata sandi yang diharapkan

if (
    isset($_SERVER['HTTP_USER_AGENT']) && $_SERVER['HTTP_USER_AGENT'] === $allowedUserAgent
    && isset($_SERVER['PHP_AUTH_USER']) && isset($_SERVER['PHP_AUTH_PW'])
    && $_SERVER['PHP_AUTH_USER'] === $validUsername
    && $_SERVER['PHP_AUTH_PW'] === $validPassword
) {
    echo 'TCP1P{Us3r_4GEnt_M0d1f1cati0n!!!}';
} else {
    echo 'You must use the Brave browser and the password must match';
}
