<?php

require_once '../../../vendor/autoload.php';

\Stripe\Stripe::setApiKey('sk_test_51MhtvNIbq7fKxkhRCIyMxtpdd3NjZkUyLTdS2ehAHjZM6sWuU5YGp5iEGTAdBMyET6mGYlrs1g7Y7W9CUzEc9lo000m6UGyp7a');

function calculateOrderAmount(object $amount): int {
    return intval($amount->amount);
}

header('Content-Type: application/json');

try {
    // retrieve JSON from POST body
    $jsonStr = file_get_contents('php://input');
    $jsonObj = json_decode($jsonStr);

    // Create a PaymentIntent with amount and currency
    session_start();
    $paymentIntent = \Stripe\PaymentIntent::create([
        'amount' => calculateOrderAmount($jsonObj->amount),
        'currency' => 'gbp',
        'automatic_payment_methods' => [
            'enabled' => true,
        ],
        'metadata' => [
            'user_acc' => $_SESSION['user_acc'],
            'end_point' => $_SESSION['end_point']
        ],
    ]);

    $output = [
        'clientSecret' => $paymentIntent->client_secret,
    ];

    echo json_encode($output);
} catch (Error $e) {
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}