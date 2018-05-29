<?php
$title = @$_REQUEST['title'];
$id=md5(rand(1,10000));
$json_obj=['id'=>$id,'title'=>$title];
#print_r($json_obj);
$json_request = json_encode($json_obj,true);

require("phpMQTT.php");

$mqtt = new phpMQTT("localhost", 1883, $id);
//Change client name to something unique

if ($mqtt->connect()) {
  $mqtt->publish("request",$json_request,0);
  echo "<!--published-->";
}
$topics[$id] = ["qos"=>0, "function"=>"myresponse"];
$mqtt->subscribe($topics,0);
while($mqtt->proc())
{
}

}//End of if isset title
function myresponse($topic, $message)
{
#global $mqtt;
#echo "Entered myresponse with $topic, $message";
  $json_obj = json_decode($message,true);
  //call the result view
include "result.php";
#$mqtt->close();
exit();
}
?>
