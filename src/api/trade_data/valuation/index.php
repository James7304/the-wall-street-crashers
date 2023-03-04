<?php

$res = array('value' => 0);
session_start();
if(isset($_SESSION['user_acc'])){

    include '../global/connection.php';

    $total_portfolio = mysqli_query($conn, "SELECT SUM(portfolio.quantity*portfolio.price_per_unit) FROM portfolio");
    $user_share = mysqli_query($conn, "SELECT share FROM users WHERE user_acc = '".$_SESSION['user_acc']."'");

    $res['value'] = mysqli_fetch_row($total_portfolio)[0] * mysqli_fetch_row($user_share)[0];

}

echo json_encode($res);

?>