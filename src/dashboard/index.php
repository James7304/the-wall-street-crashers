<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
        <link href="../assets/css/dashboard.css" rel="stylesheet">
        
        <script type="text/javascript" src="./assets/js/login.js"></script>
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
                    <button type="button" class="btn btn-outline-primary me-2">Withdraw</button>
                    <a href="../deposit"><button type="button" class="btn btn-primary">Deposit</button></a>
                </div>
            </header>
        </div>

        <div class="container mb-5">
            <div class="row">
                <div class="col-12 col-md-4">

                    <div class="card">
                        <div class="card-header">
                            Alpha Valuation
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">Valuation</h5>
                            <h3 id="alpha_value"></h3>
                            <span class="" id="alpha_return"></span>
                            <div class="spinner-border m-2" role="status" id="alpha_valuation-spinner"></div>
                        </div>
                    </div>
                    
                    <div class="card mt-3">
                        <div class="card-header">
                            Hacky Valuation
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">Valuation</h5>
                            <h3 id="hacky_value"></h3>
                            <span class="" id="hacky_return"></span>
                            <div class="spinner-border m-2" role="status" id="hacky_valuation-spinner"></div>
                        </div>
                    </div>

                    <div class="card mt-3">
                        <div class="card-header">
                            Recent Alpha Trades
                        </div>
                        <ul class="list-group list-group-flush" id="alpha_recent-trades">
                            <div class="spinner-border m-3" role="status" id="alpha_trades-spinner"></div>
                        </ul>

                    </div>

                    <div class="card mt-3">
                        <div class="card-header">
                            Recent Hacky Trades
                        </div>
                        <ul class="list-group list-group-flush" id="hacky_recent-trades">
                            <div class="spinner-border m-3" role="status" id="hacky_trades-spinner"></div>
                        </ul>

                    </div>

                </div>
                <div class="col-12 col-md-8 mt-3 mt-md-0">

                    <div class="card">
                        <div class="card-header">
                            Alpha Fund History
                        </div>
                        <div class="card-body" style="position:relative;">
                            <div class="mb-4" style="text-align:right;">
                                <a onclick="loadHistory('alpha_', 'week')" class="text-blue me-2" role="button">Week</a>
                                <a onclick="loadHistory('alpha_', 'month')" class="text-blue me-2" role="button">Month</a>
                                <a onclick="loadHistory('alpha_', 'year')" class="text-blue me-2" role="button">Year</a>
                                <a onclick="loadHistory('alpha_', 'all')" class="text-blue me-2" role="button">All time</a>
                            </div>
                            <div class="spinner-border m-3" role="status" id="alpha_history-spinner"></div>
                            <canvas id="alpha_HistoryChart"></canvas>
                        </div>
                    </div>

                    <div class="card mt-3">
                        <div class="card-header">
                            Hacky Fund History
                        </div>
                        <div class="card-body" style="position:relative;">
                            <div class="mb-4" style="text-align:right;">
                                <a onclick="loadHistory('hacky_', 'week')" class="text-blue me-2" role="button">Week</a>
                                <a onclick="loadHistory('hacky_', 'month')" class="text-blue me-2" role="button">Month</a>
                                <a onclick="loadHistory('hacky_', 'year')" class="text-blue me-2" role="button">Year</a>
                                <a onclick="loadHistory('hacky_', 'all')" class="text-blue me-2" role="button">All time</a>
                            </div>
                            <div class="spinner-border m-3" role="status" id="hacky_history-spinner"></div>
                            <canvas id="hacky_HistoryChart"></canvas>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="../assets/js/dashboard.js" type="text/javascript"></script>

    </body>
</html>