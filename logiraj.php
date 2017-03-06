<?php
function ip_addr()
{
    if (!empty($_SERVER['HTTP_CLIENT_IP']))
    {
      return $_SERVER['HTTP_CLIENT_IP'];
    }
    elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR']))
    {
      return $_SERVER['HTTP_X_FORWARDED_FOR'];
    }
    else
    {
      return $_SERVER['REMOTE_ADDR'];
    }
}

function logiraj($log)
{
	if ($log != "")
	{
		$log =  date("d.m.y H:i:s") . ", " . ip_addr() . " - " . $_SESSION['ime'] . " " . $_SESSION['priimek'] . " (" . $_SESSION['mail'] . ")\r\n" . $log . "\r\n";
		$izhod = fopen("upload.log", 'a') or die("can't open file");
		fwrite($izhod, $log);
		fclose($izhod);
	}
}
?>