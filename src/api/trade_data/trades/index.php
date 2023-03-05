<?php

include '../global/connection.php';

// Prepare and execute query to fetch all trades
$sql = "SELECT ticker, type, price, HOUR(traded_at) as hour, MINUTE(traded_at) AS minute FROM ".$_POST['end_point']."trades ORDER BY traded_at DESC LIMIT 3";
$result = mysqli_query($conn, $sql);

// Create an array to hold the trades
$trades = array();

// Loop through each trade and add it to the array
while ($row = mysqli_fetch_assoc($result)) {
    array_push($trades, $row);
}

// Convert the trades array to a JSON string
$json = json_encode($trades);

// Output the JSON string
echo $json;

// Close connection
mysqli_close($conn);

?>
