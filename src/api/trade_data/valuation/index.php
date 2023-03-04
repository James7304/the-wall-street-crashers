<?php

function percentageChange($oldValue, $newValue) {
    if ($oldValue === 0) {
      return null;
    } else {
        if($oldValue == 0){
            return 0;
        }
        $percentageChange = (($newValue - $oldValue) / $oldValue) * 100;
        return round($percentageChange, 2);
    }
}

$res = array('value' => 0);
session_start();
if(isset($_SESSION['user_acc'])){

    include '../global/connection.php';

    $total_portfolio = mysqli_query($conn, "SELECT SUM(portfolio.quantity*portfolio.price_per_unit) FROM portfolio");
    $user_share = mysqli_query($conn, "SELECT share, deposited FROM users WHERE user_acc = '".$_SESSION['user_acc']."'");

    $portfolio_row = mysqli_fetch_row($total_portfolio);
    $user_row = mysqli_fetch_row($user_share);
    $res['value'] = round($portfolio_row[0] * $user_row[0], 0);
    $res['return'] = number_format(percentageChange($user_row[1], $res['value']), 2);

}

echo json_encode($res);

?>