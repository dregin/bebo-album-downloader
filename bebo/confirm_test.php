<?php
	$username = $_POST['username'];
	$email = htmlspecialchars($_POST['email']);
	$get_original = $_POST['original'];
	if($get_original != "on")
		$get_original = "off";
	$username_stripped = preg_replace('/[^a-zA-Z0-9_]/', '', $username);
	$email_stripped = preg_replace('/[^a-zA-Z0-9@_.]/', '', $email);
	# echo "RUNNIN EXEC";
#	system("/usr/bin/python /home/associat/d/dregin/public_html/bebo/bebo_import.py $username_stripped $email_stripped >> /home/associat/d/dregin/public_html/bebo/log.txt & echo $!;");	
#	proc_close(proc_open ("python bebo_import.py $username_stripped $email_stripped	&", array(), $foo));	
#	exec("/usr/bin/python /home/associat/d/dregin/public_html/bebo/bebo_import.py $username_stripped $email_stripped")
	exec("/usr/bin/python /home/associat/d/dregin/public_html/bebo/bebo_import_test01.py $username_stripped $email_stripped $get_original > /dev/null 2>&1 &");
#	exec("/usr/bin/python /home/associat/d/dregin/public_html/bebo/bebo_import.py $username_stripped $email_stripped >> log.txt 2>&1 &");
#	echo shell_exec("/usr/bin/python /home/associat/d/dregin/public_html/bebo/bebo_import.py cianbrady dregin@gmail.com 2>&1");
	# echo "DONE EXEC";

?>
<html>
	<body>
		<?echo $get_original; ?>
		<p>
			Your request has been submitted.<br />
			A link to a zip file containing all picture albums in <?echo $username_stripped; ?>'s bebo account will be mailed to <?echo $email_stripped; ?>.
		</p>
	</body>
</html>
