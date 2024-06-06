<?php
	$destino = " .com";
	$nombre = $_POST['nombre'];
	$correo = $_POST['correo'];
	$mensaje = $_POST['mensaje'];

	$contenido = "Nombre: " . $nombre . "\nCorreo: " . $correo . "\nMensaje: " . $mensaje;

	//The function "mail" it serve for send a email
	mail($destino, "Cliente", $contenido);
	//The function "header" it serve for redirection to other site.
	header('Location: http://ricgc.com');
?>