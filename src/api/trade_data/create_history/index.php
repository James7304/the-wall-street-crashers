<?php

include '../global/connection.php';
$result = mysqli_query($conn, "SELECT type, price, traded_at FROM hacky_trades");
$valuation = 10000000;
while($row = mysqli_fetch_row($result)){
    $valuation += $row[2] * ($row['type'] == 'BUY' ? 1 : -1);
    echo $valuation . "<br>";
    mysqli_query($conn, "INSERT INTO hacky_history(valuation, time) VALUES(".$valuation.", '".$row[2]."')");
}



?>