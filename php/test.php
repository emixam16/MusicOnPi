<?php
const MAX_VOLUME= 100;
$split = explode(" ", $argv[1]);
if(count($split) == 2  /*&& $this->isInteger(-3) */ && $split[1] >= 0 && $split[1] <= MAX_VOLUME)
	exec ('echo "set volume '.$split[1].'" >../config/mpvInput');
else echo 'fail';
?>
