<?php
// webhook.php
//
// Use this sample code to handle webhook events in your integration.
//
// 1) Paste this code into a new file (webhook.php)
//
// 2) Install dependencies
//   composer require stripe/stripe-php
//
// 3) Run the server on http://localhost:4242
//   php -S localhost:4242

require '../../../../vendor/autoload.php';

// The library needs to be configured with your account's secret key.
// Ensure the key is kept out of any version control system you might be using.
$stripe = new \Stripe\StripeClient('sk_test_51MhtvNIbq7fKxkhRCIyMxtpdd3NjZkUyLTdS2ehAHjZM6sWuU5YGp5iEGTAdBMyET6mGYlrs1g7Y7W9CUzEc9lo000m6UGyp7a');

// This is your Stripe CLI webhook secret for testing your endpoint locally.
$endpoint_secret = 'whsec_I1uNxisK0NbZYAAvOO9QL10zNpxZ94sM';

$payload = @file_get_contents('php://input');
$sig_header = $_SERVER['HTTP_STRIPE_SIGNATURE'];
$event = null;

try {
  $event = \Stripe\Webhook::constructEvent(
    $payload, $sig_header, $endpoint_secret
  );
} catch(\UnexpectedValueException $e) {
  // Invalid payload
  http_response_code(400);
  exit();
} catch(\Stripe\Exception\SignatureVerificationException $e) {
  // Invalid signature
  http_response_code(400);
  exit();
}

// Handle the event
switch ($event->type) {
  case 'payment_intent.succeeded':
    $paymentIntent = $event->data->object;

    include '../../global/connection.php';

    $shares = mysqli_query($conn, "SELECT SUM(shares) FROM users");
    $value = mysqli_query($conn, "SELECT quantity * price_per_unit FROM portfolio");

    $share_price = intval(mysqli_fetch_row($value)[0])/intval(mysqli_fetch_row($shares)[0]);
    echo $share_price;

    mysqli_query($conn, "UPDATE users SET deposited = deposited + ".$paymentIntent->amount_received.", shares = shares + ".$paymentIntent->amount_received/$share_price." WHERE user_acc = '".$paymentIntent->metadata->user_acc."'");
    mysqli_query($conn, "UPDATE portfolio SET quantity = quantity + ".$paymentIntent->amount_received." WHERE ticker = 'cash'");

    break;

  default:
    echo 'Received unknown event type ' . $event->type;
}

http_response_code(200);