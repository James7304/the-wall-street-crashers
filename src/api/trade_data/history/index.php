<?php

include '../global/connection.php';

$chartTime = "all";
if(isset($_POST['chartTime'])){
    $chartTime = $_POST['chartTime'];
}

$query_condition = "";
$now = date("Y-m-d H:i:s");

if($chartTime == "week"){
    $query_condition = "WHERE time BETWEEN '".date("Y-m-d H:i:s", strtotime("-1 week"))."' AND '".$now."'";
} else if($chartTime == "month"){
    $query_condition = "WHERE time BETWEEN '".date("Y-m-d H:i:s", strtotime("-1 month"))."' AND '".$now."'";
} else if($chartTime == "year"){
    $query_condition = "WHERE time BETWEEN '".date("Y-m-d H:i:s", strtotime("-1 year"))."' AND '".$now."'";
}

// Prepare and execute query to fetch all trades
$sql = "SELECT valuation, time FROM ".$_POST['end_point']."history " . $query_condition . " ORDER BY time ASC";
$result = mysqli_query($conn, $sql);

// Create an array to hold the trades
$history = array();

// Loop through each trade and add it to the array
while ($row = mysqli_fetch_array($result)) {
    array_push($history, $row);
}

// Convert the trades array to a JSON string
$json = json_encode($history);

// Output the JSON string
echo $json;

// Close connection
mysqli_close($conn);

?>
