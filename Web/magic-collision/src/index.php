<!-- ?src -->
<?php
error_reporting(0);

if (isset($_GET['src'])) {
    die(highlight_file(__FILE__));
}

if (isset($_GET['x']) && isset($_GET['y'])){

if ($_GET['x'] != $_GET['y']) {
    if (md5($_GET['x']) == md5($_GET['y'])) {
        if (file_get_contents($_GET['tcp1p']) === 'welcome CTF TCP1P playground') {
            if (!strcmp($_GET['finish'], rand())) {
                include 'flag.php';
                echo FLAG;
            }
        }
    }
}

}
echo 'try view comment source code';

?>
