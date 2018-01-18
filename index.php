<?php

include 'generate_Playlist.php';
include 'server.php';

error_reporting(E_ALL);
ini_set('display_errors','1');


/**
 * This sample creates a channel section by :
 *
 * 1. Getting the active user's channel branding settings via "channels.list" method.
 * 2. Updating the active user's channel to show "browse view" via "channel.update" method.
 * 3. Creating a channel section in the active user's channel via "channelSections->insert" method.
 *
 * @author Ibrahim Ulukaya
*/

/**
 * Library Requirements
 *
 * 1. Install composer (https://getcomposer.org)
 * 2. On the command line, change to this directory (api-samples/php)
 * 3. Require the google/apiclient library
 *    $ composer require google/apiclient:~2.0
 */



 if (!file_exists($file = __DIR__ . '/vendor/autoload.php')) {
   throw new \Exception('please run "composer require google/apiclient:~2.0" in "' . __DIR__ .'"');
 }
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
    $redirect = filter_var('http://' . $_SERVER['HTTP_HOST'] . $_SERVER['PHP_SELF'],
    FILTER_SANITIZE_URL);

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

      header('Location: ' . $redirect);
    }

    if (isset($_SESSION[$tokenSessionKey])) {
      $client->setAccessToken($_SESSION[$tokenSessionKey]);
    }

    // Check to ensure that the access token was successfully acquired.
    if ($client->getAccessToken()) {

                file_put_contents('yt.data', serialize($youtube)    );

        return $youtube;
    }
    else {

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
/*
$OAUTH2_CLIENT_ID = '1031918371274-ipdm10odcl65lmsbhnn7img9uj4vcv0m.apps.googleusercontent.com';       // TODO Ne pas mettre ces valeurs en clair.
$OAUTH2_CLIENT_SECRET = 'LXZ09tqoSC5NAYIl_cXZIR11';
$client = new Google_Client();
$client->setClientId($OAUTH2_CLIENT_ID);
$client->setClientSecret($OAUTH2_CLIENT_SECRET);
$client->setScopes('https://www.googleapis.com/auth/youtube');
$redirect = filter_var('http://' . $_SERVER['HTTP_HOST'] . '/api/auth_success.php',
    FILTER_SANITIZE_URL);
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

  header('Location: ' . $redirect);
}
if (isset($_SESSION[$tokenSessionKey])) {
  $client->setAccessToken($_SESSION[$tokenSessionKey]);
}

// Check to ensure that the access token was successfully acquired.
if ($client->getAccessToken()) {
  try {

    /*
     * Before channel shelves will appear on your channel's web page, browse
     * view needs to be enabled. If you know that your channel already has
     * it enabled, or if you want to add a number of sections before enabling it,
     * you can skip the call to enable_browse_view().
     *

    // Call the YouTube Data API's channels.list method to retrieve your channel.

    //$listResponse = $youtube->channels->listChannels('brandingSettings', array('mine' => true));

    //$channel = $listResponse['items'][0];
    //$channel['brandingSettings']['channel']['showBrowseView'] = true;
    $videos = searchVideo($youtube, "France Gall");
    printOutput($videos);

    echo 'Génération de la playlist';
    $videos = searchVideoFromSeed($youtube, $videos[0]['id']);
    printOutput($videos);
    $videos = generatePlaylist($youtube, 'f55CqLc6IR0', 20, 20  , 0.1);
    printPlaylist($videos);

      $htmlBody = "test";
  } catch (Google_Service_Exception $e) {
    var_dump($e);
    $htmlBody = sprintf('<p>A service error occurred: <code>%s</code></p>',
        htmlspecialchars($e->getMessage()));
  } catch (Google_Exception $e) {
    $htmlBody = sprintf('<p>An client error occurred: <code>%s</code></p>',
        htmlspecialchars($e->getMessage()));
  }

  $_SESSION[$tokenSessionKey] = $client->getAccessToken();
} elseif ($OAUTH2_CLIENT_ID == 'REPLACE_ME') {
  $htmlBody = <<<END
  <h3>Client Credentials Required</h3>
  <p>
    You need to set <code>\$OAUTH2_CLIENT_ID</code> and
    <code>\$OAUTH2_CLIENT_ID</code> before proceeding.
  <p>
END;
} else {
  // If the user hasn't authorized the app, initiate the OAuth flow
  $state = mt_rand();
  $client->setState($state);
  $_SESSION['state'] = $state;

  $authUrl = $client->createAuthUrl();
  $htmlBody = <<<END
  <h3>Authorization Required</h3>
  <p>You need to <a href="$authUrl">authorize access</a> before proceeding.<p>
END;
 }
    ?>

    <!doctype html>
    <html>
    <head>
    <title>Section Created</title>
    </head>
    <body>
        <?=$htmlBody?>
    </body>
    </html>
*/
