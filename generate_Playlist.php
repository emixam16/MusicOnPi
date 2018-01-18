<?php
    include_once 'search_video.php';
    /// Generates a playlist from a single seed.
    function generatePlaylist($youtube, $seed, $depth, $nbSuggestions, $probaReturn)
    {
        $ans = array();
        for($i=0; $i<$depth; $i+=1)
        {
            $raw_ans = searchVideoFromSeed($youtube, $seed);
            $offset = rand ( 0,  count($ans)-1 );
            $ans[$i] = $raw_ans[$offset];
            $seed = getRealSeed($ans, $probaReturn);
            //var_dump($seed);
        }

        //die(var_dump($ans));
        return $ans;
    }

    function printPlaylist($playlist)
    {
        for($i=0; $i<count($playlist);$i+=1)
            echo "<p> Video title ". $playlist[$i]["title"].". Video id = ". $playlist[$i]["id"]. "</p>";
    }
    function getRealSeed($ans, $probaReturn) {
        $val = rand() / getrandmax();
        $i = count($ans)- 1;   // On part de la dernière case
        while ($val < $probaReturn && $i > 0) {
            $val /= $probaReturn;
            $i -= 1;
        }
        return $ans[$i]["id"];
    }
?>
