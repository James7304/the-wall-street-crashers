
<?php

include '../global/connection.php';


// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

$res = array('login' => false);

// Check if email and password were sent in POST request
if(isset($_POST['email']) && isset($_POST['password'])){

    // Get email and password from POST request
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Encrypt password using SHA512
    $encrypted_password = hash('sha512', $password);

    // Prepare and execute query to fetch user from database
    $sql = "SELECT * FROM users WHERE email = '".$email."' AND password = '".$encrypted_password."'";
    $result = mysqli_query($conn, $sql);

    // Check if user was found
    if (mysqli_num_rows($result) > 0) {
        $res = array('login' => true);
        session_start();
        $_SESSION['user_acc'] = mysqli_fetch_array($result)['user_acc'];
    }

}

// Close connection
mysqli_close($conn);

echo json_encode($res);

?>