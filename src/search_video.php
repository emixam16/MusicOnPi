<?php

function searchVideo($youtube, $query) {
    $searchResponse = $youtube->search->listSearch('id,snippet', array(
        'q' => $query,
        'type' => 'video',
        'maxResults' => 10
    ));
  	$out=[[]];
    for ($i=0; $i < count($searchResponse['items']); $i++)
    {
        $ans = $searchResponse['items'][$i];
        $out[$i]['title'] = $ans['snippet']['title'];
        $out[$i]['id'] = $ans['id']['videoId'];
    }
    return $out;
}

function searchVideoFromSeed($youtube, $seed) {
    $searchResponse = $youtube->search->listSearch('id,snippet', array(
        'relatedToVideoId' => $seed,
        'type' => 'video',
        'maxResults' => 20
    ));
  	$out=[[]];
    for ($i=0; $i < count($searchResponse['items']); $i++)
    {
        $ans = $searchResponse['items'][$i];
        $out[$i]['title'] = $ans['snippet']['title'];
        $out[$i]['id'] = $ans['id']['videoId'];
    }
    return $out;
}

function printOutput($output)
{
    for ($i=0; $i < count($output); $i++)
    {
        $ans = $output[$i];
        echo '<p><a href=https://www.youtube.com/watch?v='.$ans['id'].">$ans[title]</a> . Id de la vidéo: $ans[id] </p>\n";


    }
}
