<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $validUsers = array(
        "user1" => "password1",
        "user2" => "password2",
        "user3" => "password3"
    );

    $inputUsername = $_POST["username"];
    $inputPassword = $_POST["password"];

    if (array_key_exists($inputUsername, $validUsers) && $validUsers[$inputUsername] === $inputPassword) {
        $_SESSION['username'] = $inputUsername;
        header('Location: index.php');
        exit();
    } else {
        $errorMessage = "Invalid username or password.";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <?php
    if (isset($errorMessage)) {
        echo '<p style="color: red;">' . $errorMessage . '</p>';
    }
    ?>
    <form method="POST" action="login.php">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username"><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password"><br><br>

        <input type="submit" value="Login">
    </form>
</body>
</html>
