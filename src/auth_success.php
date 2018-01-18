<?php
 require_once __DIR__ . '/vendor/autoload.php';
  session_start();
function Auth()
{
    $OAUTH2_CLIENT_ID = '1031918371274-ipdm10odcl65lmsbhnn7img9uj4vcv0m.apps.googleusercontent.com';       // TODO Ne pas mettre ces valeurs en clair.
    $OAUTH2_CLIENT_SECRET = 'LXZ09tqoSC5NAYIl_cXZIR11';

    $client = new Google_Client();
    $client->setClientId($OAUTH2_CLIENT_ID);
    $client->setClientSecret($OAUTH2_CLIENT_SECRET);
    $client->setScopes('https://www.googleapis.com/auth/youtube');
    $redirect = filter_var('http://' . $_SERVER['HTTP_HOST'] .'/api/auth_success.php', FILTER_SANITIZE_URL);
    $client->setRedirectUri($redirect);
    // Define an object that will be used to make all API requests.
    $youtube = new Google_Service_YouTube($client);

    // Check if an auth token exists for the required scopes
    $tokenSessionKey = 'token-' . $client->prepareScopes();
    if (isset($_GET['code'])) {
      if (strval($_SESSION['state']) !== strval($_GET['state'])) {
        die('The session state did not match.');
      }

      $client->authenticate($_GET['code']);
      $_SESSION[$tokenSessionKey] = $client->getAccessToken();

      $GLOBALS['youtube'] = $youtube;
      header('Location: ' . $redirect);
    }

    if (isset($_SESSION[$tokenSessionKey])) {
      $client->setAccessToken($_SESSION[$tokenSessionKey]);
    }
 die('bef');
    // Check to ensure that the access token was successfully acquired.
    if ($client->getAccessToken()) {
 die('at');
            $GLOBALS['youtube'] = $youtube;
            var_dump($GLOBALS['youtube']);
        return $youtube;
    }
    else {
        die('nat');
    //    die( "acctok");
      // If the user hasn't authorized the app, initiate the OAuth flow
      $state = mt_rand();
      $client->setState($state);
      $_SESSION['state'] = $state;

      $authUrl = $client->createAuthUrl();
      //die($authUrl);
       /// header('Location: ' . $authUrl); // MODE redirection automatique
      echo "You need to <a href=$authUrl>authorize access</a> before proceeding.<p>";
     }

}
Auth();
?>
