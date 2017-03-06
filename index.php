<?php session_start(); ?>

<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=windows-1250">
  <title>Svitov FotoStorming</title>
  <link rel="Stylesheet" type="text/css" href="svit.css" />

<?php 
//////////////////
$STEVILO_SLIK = 3;
//////////////////

$niz = "[";
for ($i = 1; $i <= $STEVILO_SLIK; $i++) {
    $niz .= "\"slika" . $i . "\"";
	if ($i < $STEVILO_SLIK)
		$niz .= ", ";
}
$niz .= "]";
?>

<script type="text/javascript">
<!--
  function preveri()
  {
	var napaka = 0;
	var opozorilo = "";
	
	var polja = ["ime", "priimek", "mail"];

    for (i=0;i<3;i++)
	{
  	  if (document.getElementById(polja[i]).value == "") 
	  {
	    document.getElementById(polja[i]).className = "napaka";
	    napaka = 1;
	  }
	}
	
	if (napaka == 1)
	{
	  opozorilo += "Prosim izpolnite vse podatke!<br/>";	
	}
	
	var j = 0;
	var koncnice = ["JPG", "JPEG"];
	polja = <?php echo $niz; ?>;

    for (i=0;i<<?php echo $STEVILO_SLIK; ?>;i++)
	{
	  var slika = document.getElementById(polja[i]).value;
	  if (slika != "")
	  {
	    j++;
	    if (koncnice.indexOf(slika.split('.').pop().toUpperCase()) == -1)
	    {
		  napaka = 2;
    	  document.getElementById(polja[i]).className = "napaka";
	    }
  	  }
	}

	if (napaka == 2)
	{
	  opozorilo += "Datoteke morajo biti v JPG formatu!<br/>";	
	}
	
	if (j == 0)
	{
	  document.getElementById("slika1").className = "napaka";
	  napaka = 3;
  	  opozorilo += "Naložite vsaj eno datoteko!<br/>";	
	}
	
	document.getElementById('opozorilo').innerHTML = '<p>' + opozorilo + '</p>';
	
	if (napaka) {return false;}
	else {return true;}
  }

  function popravi(a)
  {
	a.className = "";
  }
-->
</script>

</head>

<body>


<?php

date_default_timezone_set("Europe/Ljubljana");

require 'logiraj.php';

$izhod = fopen("dostop.log", 'a') or die("can't open file");
fwrite($izhod, date("d.m.y H:i:s") . " - " . ip_addr() . "\r\n");
fclose($izhod);

if(isset($_SESSION["shranjene"]))
{
	$log = "";
	foreach($_SESSION["shranjene"] as $id => $ime)
	{
		unlink($ime);
		$log .= $ime . "  IZBRISANO\r\n";
	}
	logiraj($log);

	unset($_SESSION["shranjene"]);
}

?>


<div>
	
    <p style="text-align:justify">Fotografije naj bodo v JPG formatu in naj ne presegajo <span style="font-size:20px; color:red; font-weight:bold">2000px</span> po daljši stranici oz. <span style="font-size:20px; color:red;  font-weight:bold">2MB</span> po velikosti. V kolikor ne želite, naslovov ni treba vpisati.
        
    <form enctype='multipart/form-data' action='upload.php' onSubmit="return preveri();" method='POST'>

        <label>Ime:</label> 
        <input name='ime' id='ime' type='text' onFocus='popravi(this);' />
 	    
        <label>Priimek:</label>
        <input name='priimek' id='priimek' type='text' onFocus='popravi(this);' />
  	    
        <label>Email:</label>
        <input name='mail' id='mail' type='text' onFocus='popravi(this);' />
        
        <label>Fotostorming:<br /></label>
        <div id='fotostorming' class='fotostorming'>
<!--
            <input type='radio' name='storming' id='storming' value='Toskana' />Toskana<br />
-->
            <input type='radio' name='storming' id='storming' value='magnet' checked/>Magnet<br />
 	</div>
        
		<?php 
    	for ($i = 1; $i <= $STEVILO_SLIK; $i++) 
		{
			echo $i . ". slika: <input name='slika" . $i . "' id='slika" . $i . "' type='file' accept='image/jpeg' onClick='popravi(this);' />";
        	echo "<input name='slika" . $i . "nasl' id='slika" . $i . "nasl' type='text' placeholder='Naslov' />";
		}
		?>

        <div id='opozorilo' class='opozorilo'>
        <?php
		if(isset($_SESSION["napaka"]))
		{
			echo "<p>" . $_SESSION["napaka"] . "</p>";
			unset($_SESSION["napaka"]);
		}
		?>        
        </div>

        <input type='submit' value='Naloži' />
        
        
    </form>

    <p style="font-size:10px; text-align:center">Ta spletna stran uporablja sejni piškotek <i>PHPSESSID</i>, ki ga je, po drugem odstavku 157. člena ZEKom-1, dovoljeno uporabljati po načelu domnevne privolitve.</p>

</div>

<?php
		if(isset($_SESSION["opozorila"]))
		{
			echo "<script type='text/javascript'>";
			foreach($_SESSION["opozorila"] as $id => $opozorilo)
				echo "document.getElementById('" . $opozorilo . "').className = 'napaka';";
			echo "</script>";
		}

?>


</body>
</html>
