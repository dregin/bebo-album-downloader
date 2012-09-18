<html>
	<head>
		<link rel="stylesheet" href="style.css" type="text/css"> 
	</head>
	<body>
		<form action="confirm.php" method="post">
			<div id="container" style="align:center;border:1px solid black; padding:10px">
				<font color=red>NOTE:</font> For now this only works on PUBLIC profiles.<br>
				You must set your profile to public in order to use this app. You can set it back to private once you've been mailed the link to the zip file :-)
				<ul>
					<li>Enter the bebo username whose photo albums you want to download.</li>
					<li>Enter the email which will receive a link to the zip file containing the photo albums.</li>
				</ul>
				<div><label for="username">Bebo Username:</label> <input type="text" name="username"/></div><br />
				<div><label for="email">E-Mail:</label><input type="text" name="email"/></div><br />
				<font color=red>*NEW* </font>Download original (larger) images? <input type="checkbox" name="original"><br />
				<br>
				This is still a work in progress.<br>
				It will soon be able to take login details in order to grab photos from profiles that are marked private.<br>
				Any feedback welcome to dregin@redbrick.dcu.ie<br />
			</div>
			<br>
			<div>
				<input type="submit" value="Submit">
			</div>
		</form>
	</body>
</html>
