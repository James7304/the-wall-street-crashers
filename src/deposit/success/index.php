<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Desposit Success</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
        <link href="../../assets/css/dashboard.css" rel="stylesheet">
        
    </head>
    <body>

        <?php

            session_start();
            if(!isset($_SESSION['user_acc'])){
                header('Location: ../');
            }

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
                    Deposit Success
                </div>
                <div class="card-body">
                    <h5 class="card-title"><b>£<?php echo intval($_GET['amount'])/100 ?></b> has successfully been deposited into your account</h5>
                    <a href="../../../dashboard">Go back to your dashboard</a>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    </body>
</html>