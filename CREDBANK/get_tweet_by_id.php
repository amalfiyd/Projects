<?php 
	require_once("TwitterAPIExchange.php");
	$myfile = fopen("cred_event_SearchTweets.data", "r") or die("Unable to open file!");
	fgets($myfile);

		// Only first row of the data is served
  		$line = fgets($myfile) . "<br>";
  		$temp = explode("\t", $line);

  		echo "Topic : " . $temp[1] . "</br>";

  		$count = $temp[2];
  		// $object = substr($temp[3], 1);
  		// $object = substr($object, 0,-6);
  		$object = trim($temp[3], '[]');
  		$iter = 1;
  		foreach(preg_split('/\)\,\ \(/', $object) as $row)
  		{
  			$temp = trim($row, "(");
  			$temp = str_replace(")]", "", $temp);
  			$temp = str_replace("'", "", $temp);
  			$splits = explode(", ", $temp);
  			$id_string = explode("=", $splits[0])[1];

  			// echo $temp . "</br>";
  			// echo $id_string;

  			$settings = array(
			    'oauth_access_token' => "178696682-TPEFTYUOM7i9MZbqejpEdOdFna0pS3dIRiS4CghG",
			    'oauth_access_token_secret' => "OxBWTQjSfuUAM1XTjCuKo6J3eu3ctfrkkAdB8RZW73ve9",
			    'consumer_key' => "aMyGXiYsbEwvcc9muEyVtBXSz",
			    'consumer_secret' => "sw6kaxleO9sUPbDoqqYRB0qvjswkV2ij8KlXButAcf4eiCYo3L"
			);

			$url = 'https://api.twitter.com/1.1/statuses/show.json';
			$getfield = '?id='.$id_string;
			$requestMethod = 'GET';

			$twitter = new TwitterAPIExchange($settings);
			$response = $twitter->setGetfield($getfield)
			             ->buildOauth($url, $requestMethod)
			             ->performRequest();

			$object = json_decode($response);
			if(!isset($object->errors))
			{
				echo $object->id . ",";
				echo str_replace(",", " ", $object->text) . "</br>";
			}

			if($iter == 25)
			{
				break;
			}
			$iter++;
  		}

	fclose($myfile);
?>