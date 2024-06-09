<?php
    // Database credentials
    $servername = "localhost";
    $username = "ebaveromar_roboticmeteo";  // Replace with your database username
    $password = "G1rP0w3r!3n4.D14n4#Lu4";      // Replace with your database password
    $dbname = "ebaveromar_roboticmeteo"; // Replace with your database name

    // Create a connection to the database
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check the connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Retrieve GET parameters
    $station_id = isset($_GET['ID']) ? $_GET['ID'] : '';
    $temp_f = isset($_GET['tempf']) ? $_GET['tempf'] : '';
    $humidity = isset($_GET['humidity']) ? $_GET['humidity'] : '';
    $baro_min = isset($_GET['baromin']) ? $_GET['baromin'] : '';
    $wind_speed_mph = isset($_GET['windspeedmph']) ? $_GET['windspeedmph'] : '';
    $wind_gust_mph = isset($_GET['windgustmph']) ? $_GET['windgustmph'] : '';
    $dewpt_f = isset($_GET['dewptf']) ? $_GET['dewptf'] : '';
    $rain_in = isset($_GET['rainin']) ? $_GET['rainin'] : '';
    $date_utc = isset($_GET['dateutc']) ? $_GET['dateutc'] : '';

    // Convert units if necessary (e.g., temperature from Fahrenheit to Celsius, pressure from inHg to hPa)
    // Assuming temperature is in Fahrenheit and pressure is in inHg for demonstration purposes
    $temperature = ($temp_f - 32) / 1.8;  // Fahrenheit to Celsius
    $pressure = $baro_min / 0.0295300;    // inHg to hPa
    $wind_speed = $wind_speed_mph / 0.6213711922; // mph to m/s
    $wind_gust = $wind_gust_mph / 0.6213711922; // mph to m/s
    $dew_point = ($dewpt_f - 32) / 1.8; // Fahrenheit to Celsius
    $rainfall = $rain_in / 0.0393701; // inches to mm

    // Prepare the SQL statement
    $stmt = $conn->prepare("INSERT INTO weather_data (station_id, temperature, humidity, pressure, wind_speed, wind_gust, dew_point, rainfall, date_utc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("sdddddddd", $station_id, $temperature, $humidity, $pressure, $wind_speed, $wind_gust, $dew_point, $rainfall, $date_utc);

    // Execute the statement
    if ($stmt->execute()) {
        echo "Data inserted successfully.";
    } 
    else {
        echo "Error: " . $stmt->error;
    }

    // Close the statement and the connection
    $stmt->close();
    $conn->close();
?>