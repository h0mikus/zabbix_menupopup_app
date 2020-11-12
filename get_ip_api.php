<?php
$hostid = $_POST['hostid'];

if ($hostid == '')
  $hostid = 0;

$url = 'http://127.0.0.1/api_jsonrpc.php';


$login = 'API_user';
$password = 'API_password';

$params = array(
  'jsonrpc' => '2.0',
  'method' => 'user.login',
  'params' => array(
    'user' => $login,
    'password' => $password
  ),
  'id' => 1,
  'auth' => null
);

$result = json_decode(file_get_contents($url, false, stream_context_create(array(
  'http' => array(
    'method'  => 'POST',
    'header'  => 'Content-type: application/json',
    'content' => json_encode($params)
  )
))), true);

$api_key = $result["result"];

$params = array(
    'jsonrpc' => '2.0',
    'method' => 'hostinterface.get',
    "params" => array("hostids" => $hostid),
    'auth' => $api_key,
    'id' => 2
);

$result = json_decode(file_get_contents($url, false, stream_context_create(array(
  'http' => array(
    'method'  => 'POST',
    'header'  => 'Content-type: application/json',
    'content' => json_encode($params)
  )
))), true);

$ip = $result['result'][0]['ip'];

echo $ip;
?>