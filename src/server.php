<?php
include_once 'search_video.php';
require_once __DIR__ . '/vendor/autoload.php';
session_start();

const MAX_VOLUME = 10;
const PLAYLIST_LENGTH = 10;

class Main {
    public  $youtube = null;
    private function isInteger($input)
    {
        if(is_string($input) && $input[0] == '-')   // Nombres négatifs (TODO gérér la même chose avec les nombres.)
            $input = substr($input, 1);
        return(ctype_digit(strval($input)));
    }
    public function Rest($cmd) {
        try {
            //var_dump($GLOBALS);
            $this->youtube = unserialize(file_get_contents('yt.data'));
            //$videos = searchVideo($this->youtube, "France Gall");
            //var_dump($videos);
            $cmd = htmlspecialchars($cmd);
            $split = explode(" ", $cmd);
            switch ($split[0]) {
            case 'volume':
                if(count($split) == 2  /*&& $this->isInteger(-3) */ && $this->isInteger($split[1]) && $split[1] >= 0 && $split[1] <= MAX_VOLUME)
                    echo "<p>ok</p>";
                else throw new Exception('Bad option for volume');
            break;
            case 'search':      // TODO vérifier plus en profondeur les graines passées pour éviter les 'blagues'
                if(count($split) == 2)
                {
                    $var = substr($cmd, strlen('search')+1);
                    if($var == '' || ctype_space($var)) throw new Exception('Bad option for search');
                    //var_dump(searchVideo($this->youtube,$var));
                echo json_encode(searchVideo($this->youtube,$var));
                }
                else throw new Exception('Bad option for search');
            break;
            case 'generate':      // TODO vérifier plus en profondeur les graines passées pour éviter les 'blagues'
                if(count($split) == 2)
                {
                    $var = substr($cmd, strlen('generate')+1);
                    if($var == '' || ctype_space($var)) throw new Exception('Bad option for generate');
                    echo "<p>$var</p>";
                }
                else throw new Exception('Bad option for search');
            break;
            case 'addmusic':
                if(count($split) == 2) // On ne peut pas se supprimer soi même
                {
                    $var = substr($cmd, strlen('addmusic')+1);
                    if($var == '' || ctype_space($var)) throw new Exception('Bad option for search');
                    echo "<p>$var</p>";
                }
                else throw new Exception('Bad option for delete');
            break;
            case 'delete':
                if(count($split) == 2  && $this->isInteger($split[1]) && $split[1] > 0 && $split[1] <= PLAYLIST_LENGTH) // On ne peut pas se supprimer soi même
                    echo "ok";
                else throw new Exception('Bad option for delete');
            break;
            case 'setmusic':
                echo "s1:$split[1]";
                if(count($split) == 2  && $this->isInteger($split[1]) && $split[1] >= -PLAYLIST_LENGTH && $split[1] <= PLAYLIST_LENGTH)
                    echo "ok";
                else throw new Exception('Bad option for setmusic');
            break;
            case 'start':
                if(count($split) == 1)
                    echo "ok";
                else throw new Exception('Bad option for start');
            break;
            case 'stop':
                if(count($split) == 1)
                    echo "ok";
                else throw new Exception('Bad option for setmusic');
            break;
            default: throw new Exception('Unknown command');
            break;
            }
        }
        catch (\Exception $e)
        {
            echo "Exception " . $e->getMessage();
        }
    }
}
?>
