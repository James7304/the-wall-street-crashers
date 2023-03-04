<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Desposit</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
        <link href="../../../+assets/css/dashboard.css" rel="stylesheet">
        
        <script src="https://js.stripe.com/v3/"></script>
        <script src="../pay/scripts/checkout.js" defer></script>
    </head>
    <body>

        <?php

            session_start();
            if(!isset($_SESSION['user_acc']) || !isset($_GET['amount']) || !isset($_GET['end-point'])){
                header('Location: ../../');
            }

            session_start();
            $_SESSION['end-point'] = $_GET['end-point'];

        ?>
        
        <div class="container">
            <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
                <a href="./" class="d-flex align-items-center col-6 mb-2 mb-md-0 text-dark text-decoration-none">
                    <h2 class="title-logo">The Wall Street Crasher</h2>
                </a>

                <div class="col-md-3 text-end">
                    <a href="../dashboard"><button type="button" class="btn btn-primary">Home</button></a>
                </div>
            </header>
        </div>

        <div class="container">
            <div class="card">
                <div class="card-header">
                    Checkout
                </div>
                <div class="card-body">
                    <!-- Display a payment form -->
                    <form id="payment-form">
                        <div id="link-authentication-element">
                            <!--Stripe.js injects the Link Authentication Element-->
                        </div>
                        <div id="payment-element">
                            <!--Stripe.js injects the Payment Element-->
                        </div>
                        <button id="submit" class="btn btn-primary mt-3">
                            <div class="spinner hidden" id="spinner"></div>
                            <span id="button-text">Deposit</span>
                        </button>
                        <div id="payment-message" class="hidden"></div>
                    </form>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    </body>
</html>