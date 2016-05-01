#!"C:\Perl64\bin\perl.exe"


#
#   This is pulling my cases using the details rest query
#   More info here : https://cisco.jiveon.com/docs/DOC-194000
#   Some look up links, although not working as of 17/11/15
#	
#	This script should return a JSON format list of P1 and P2 cases open in Remedy 8.
#	Also provides a LOT of extra detail

#
#	Update:  Going to change this script to write the p1p2 data to a swap file.  Updating every 15mins or so.
#

use cgi;
use LWP::UserAgent;
use HTTP::Request::Common;
use MIME::Base64;
use JSON::Parse;

# used for loading custom library
use FindBin qw($Bin);
use lib "$Bin/../lib";	
use Common;


# Code for access resources on different Env
use Sys::Hostname;
my $host = hostname;
my %dynSmartdataAccounts;
if ($host eq "SMT-APL-001-D"){
	%dynSmartdataAccounts = %smartdataAccounts_DEV
}
if ($host eq "SMT-AUT-001-S"){
	%dynSmartdataAccounts = %smartdataAccounts_STAGE
}
if ($host eq "SMT-AUT-001-P"){
	%dynSmartdataAccounts = %smartdataAccounts_PROD
}


# Set password for Remedy API
my $R8un = $dynSmartdataAccounts{'R8un'};
my $R8pw = decode_base64($dynSmartdataAccounts{'R8pw'});



$c = new CGI;
if ($c->param()) {
	$callback = $c->param('callback');	
}


print 'Access-Control-Allow-Methods: GET';

# Headers for JSONP
if ($callback) {
  print "Content-type: application/javascript\n\n";
} else {
  print "Content-type: application/json\n\n";
}




#
#	So.... checkFileDate
#	If File does not exsist or is older than 10mins  -> Update file
#	
#	sub print file results
#
my $destination = "$Bin/../shared/";
my $p1p1FileName = "p1p2.json";

$p1p1FileName = $destination . $p1p1FileName;



&main;


sub main {
	my $response;
	
	my $modtime = getModifiedTime($p1p1FileName);
	if ($modtime > 600 ){	# 36000 is 10mins?  60sec in 1 min, 1  
		# Get p1p2 data
		$response = &getp1p2Data;		
		if (&checkValidJSON($response)){			# If the returned is not valid JSON it does not overwrite the file.
			&writetoFile($p1p1FileName, $response );
		}
	}
	
	$response = &readFromFile($p1p1FileName); 
	&outputReponse($response);

}

exit;


sub getModifiedTime {
	# Takes filename with path and returns how long since the file was modified in sec.
	# If the file does not exist then the time is epoch
	my ($filename) = @_;
	
	my $currenttime = time();
	my $epoch_timestamp = (stat($filename))[9];
	return $currenttime - $epoch_timestamp;
}



sub writetoFile {
	# Writes output to local file with the filename and path $filename			
	my ($filename, $output) = @_;
	#print "*** Writing to file: $filename \n ";
	open(OUT, ">$filename") or &die("Couldn't open to write file $filename: $!");
	print OUT $output;
	close(OUT);

}

sub readFromFile {
	# Reads the file and return all contents !! Do NOT use on big files
	my ($filename) = @_;
	my $response;
	#print "*** Reading from file: $filename ";
	open(IN, "$filename") or &die("Couldn't open to read file $filename: $!");
	while (my $row = <IN>) {
		  $response .= $row;
		  
		}
	close(IN);
	return $response; 

}




sub getp1p2Data {
	# Get the p1p2Data : return decoded content or exit with status 0
	BEGIN { $ENV{PERL_LWP_SSL_VERIFY_HOSTNAME} = 0 }
	my($ua) = LWP::UserAgent->new;
	my $credentials=MIME::Base64::encode(join(":",$R8un,$R8pw));

	$req = POST 'https://wsgx.cisco.com/remedy/service/arservice/remedyintegration/get/incident/details',
				[
				'QualificationQuery' => "('Status' = \"NEW\" OR 'Status' = \"ASSIGNED\" OR 'Status' = \"IN PROGRESS\" OR 'Status' = \"PENDING\") AND ('Priority' = \"P1\" OR 'Priority' = \"P2\")"
				];

	$req->header("Authorization" => "Basic $credentials");
	my $response = $ua->request($req);

	if ($response->is_success ) {
				#print $response->decoded_content;
				return $response->decoded_content;
		}
	else{
	
			print '{"status" : 0}';
		}
}

sub checkValidJSON {
	# This check input, if valid JSON it return 1 (true) if not 0 (false)
	my ($json) = @_;
	use JSON::Parse 'valid_json';
		if (valid_json ($json)) {
			return 1; 
		}else{
			return 0;
		}
}

sub outputReponse{
	# Outputs JSONP if callback set
	# Outputs readable on DEV hosts
	# Outputs status 0 on other hosts
	my ($json) = @_;

		if ($callback) {
			print $callback . '(' . $json . ');';
		} elsif ($dynSmartdataAccounts{'env'} eq 'DEV') {
			print $json,"\n";
		}else {
			print '{"status" : 0}';

		}
}