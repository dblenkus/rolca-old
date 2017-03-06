<?php session_start(); ?>

<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=windows-1250">
  <title>Svitov FotoStorming</title>
  <link rel="Stylesheet" type="text/css" href="svit.css" />
</head>

<body>

<?php

date_default_timezone_set("Europe/Ljubljana");

require 'logiraj.php';

function nazaj($napaka)
{
	echo "<script type='text/javascript'>history.go(-1)</script>";
	$_SESSION["napaka"] = $napaka;
}

$_SESSION["ime"] = $_POST["ime"];
$_SESSION["priimek"] = $_POST["priimek"];
$_SESSION["mail"] = $_POST["mail"];
$_SESSION["shranjene"] = array();
$_SESSION["opozorila"] = array();

$napaka = 0;
$log = "";
$seznam = array();
$i = 1;
while(isset($_FILES["slika" . $i]["error"]))
{
	$seznam[$i] = array();
	$seznam[$i]["id"] = "slika" . $i;
	$seznam[$i]["naslov"] = $_POST["slika" . $i . "nasl"];
	$i++;
}

if (in_array("", array($_POST['ime'], $_POST['priimek'], $_POST['mail']))) #pogleda, če so izpolnjena vsa polja
{
	$napaka = 1;	
	nazaj("Prosim izpolnite vsa polja s podatki!");
}

if (!$napaka)
{
	foreach( $seznam as $id => $slika) #gre čez vse slike in pogleda katere so naložene
	{
    	if ($_FILES[$slika["id"]]["error"] != 0) #pogleda, če je fotka pravilno naložena
			unset($seznam[$id]); #nenaložene fotke odstrani iz seznama
		else
		{
        	$ext = pathinfo($_FILES[$slika["id"]]["name"],PATHINFO_EXTENSION); #dobi končnico datoteke
			if ((!(in_array($_FILES[$slika["id"]]["type"], array("image/jpeg", "image/pjpeg")))) || (!(in_array(strtoupper($ext), array("JPG", "JPEG")))))	#preveri, če je datoteka jpg
			{
				$napaka = 2;
				$log .= "Datoteka:" . $_FILES[$slika["id"]]["name"] . " Tip:" . $_FILES[$slika["id"]]["type"] . " Končnica:" . $ext . "\r\n";
				$_SESSION["opozorila"][] = $slika["id"];
			}
			else
			{
				$resolucija = array_slice(getimagesize($_FILES[$slika["id"]]["tmp_name"]), 0, 2); #dobi array z resolucijo fotke (wxh)
				if (($_FILES[$slika["id"]]["size"] >= 2097152) || (max($resolucija) > 2000))	
				{
					if ($napaka != 2) {$napaka = 3;} #opozorilo za napačen format ima prednost pred opozorilom za velikost
					$log .= "Datoteka:" . $_FILES[$slika["id"]]["name"] . " Velikost:" . $_FILES[$slika["id"]]["size"] . "B Resolucija:" . $resolucija[0] . "x" . $resolucija[1] . "\r\n";
					$_SESSION["opozorila"][] = $slika["id"];
				}
			}
		}
	}
}

if ($napaka)
{
	if ($napaka == 2)
	{
    	logiraj("ERROR! \r\n" . $log);	
		nazaj("Prosim naložite datoteko v jpg formatu! \r\n");
	}
	elseif ($napaka == 3)
	{
    	logiraj("ERROR! \r\n" . $log);	
		nazaj("Prevelika datoteka! \r\n");
	}
}
else
{	

	if ($seznam == array()) #pogleda, če je naložena vsaj ena fotka
		nazaj("Nobena datoteka ni izbrana");
	else
	{
		$sirina = count($seznam);
		echo "<div style='width: " . ($sirina*300) . "px;'>";
		
		echo "<div><form>";
		echo "<label>Ime:</label> <input type='text' value='" . $_POST["ime"] . "' size='10' disabled />";
		echo "<label>Priimek:</label> <input type='text' value='" . $_POST["priimek"] . "' size='10' disabled />";
		echo "<label>Email:</label> <input type='text' value='" . $_POST["mail"] . "' size='10' disabled />";
		echo "</form></div>";	

		echo "<div class='tabela'>";

		echo "<div class='vrstica'>";
		foreach( $seznam as $id => $slika) #gre čez vse naložene fotke
		{
			$pot = "uploads/" . str_replace(' ', '_', $_POST["storming"]);;
			
			if ($slika["naslov"] != "")
				$ime = $_POST["ime"] . $_POST["priimek"] . "_" . time() . "-" . $id . "-" . $slika["naslov"] . ".jpg"; #naredi novo ime fotke
			else
				$ime = $_POST["ime"] . $_POST["priimek"] . "_" . time() . "-" . $id . ".jpg"; #naredi novo ime fotke
				
			$ime = str_replace(' ', '_', $ime);

			if (!is_dir($pot)) mkdir($pot); #naredi mapo, če še ne obstaja

			move_uploaded_file($_FILES[$slika["id"]]["tmp_name"], $pot . "/" . $ime);	#skopira fotko
			
			$_SESSION["shranjene"][] = $pot . "/" . $ime;
			
			$log .= $pot . "/" . $ime . " (" . $_FILES[$slika["id"]]["name"] . ")  NALOŽENO\r\n";
			
			echo "<div class='celica'>";
			
			$velikost = getimagesize($pot . "/" . $ime);
			if ($velikost[0] < $velikost[1]) #poskrbi, da je fotka velika 295px po daljši stranici
				echo "<img src='" . str_replace('%2F', '/', urlencode($pot)) . "/" . urlencode($ime) . "' height='295' />"; 
			else
				echo "<img src='" . str_replace('%2F', '/', urlencode($pot)) . "/" . urlencode($ime) . "' width='295' />"; 
			
			echo "</div>";
		}
		echo "</div>";

		echo "<div class='vrstica'>";
		foreach( $seznam as $id => $slika) #gre čez vse naložene fotke
		{
			echo "<div class='celica'>";
			if ($slika["naslov"] != "")
			echo "<form><input type='text' class='naslov' value='" . $slika["naslov"] . "' disabled /></form>";		
			echo "</div>";

		}
		echo "</div>";

		echo "</div>";
		
		echo "<div>";
		echo "<div class='levo'><form>"; #gumb za zahvalno sporočilo in za nazaj
		echo "<input type='button' value='Nazaj' onClick='history.go(-1)' />";
		echo "</form></div>";
		echo "<div class='desno'><form>";
		echo "<input type='button' value='Konec' onclick='location.href=\"konec.php\"' />";
    	echo "</form></div>";
		echo "</div>";

		echo "</div>";
		
		logiraj($log);
	}
}

?>

</body>