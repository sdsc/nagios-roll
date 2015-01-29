#!/usr/bin/perl -w
# nagios roll installation test.  Usage:
# nagios.t [nodetype]
#   where nodetype is one of "Compute", "Dbnode", "Frontend" or "Login"
#   if not specified, the test assumes either Compute or Frontend

use Test::More qw(no_plan);

my $appliance = $#ARGV >= 0 ? $ARGV[0] :
                -d '/export/rocks/install' ? 'Frontend' : 'Compute';
my $output;

# nagios-doc.xml
SKIP: {
  skip 'not server', 1 if $appliance ne 'Frontend';
  ok(-d '/var/www/html/roll-documentation/nagios-roll', 'doc installed');
}

# nagios-server.xml
SKIP: {

  skip 'not server', 16 if $appliance ne 'Frontend';
  ok(-d '/opt/nagios', 'nagios installed');
  ok(-f '/opt/nagios/libexec/check_dummy', 'nagios plugins installed');
  $output = `rocks dump nagios 2>&1`;
  ok($? == 0, 'nagios rocks commands defined');
  `grep -q '^nagios:' /etc/passwd 2>&1`;
  ok($? == 0, 'nagios user created');
  $output = `id nagios 2>&1`;
  like($output, qr/apache/, 'nagios in group apache');
  $output = `service nagios status 2>&1`;
  ok($? == 0, 'nagios service defined');
  like($output, qr/running/, 'nagios running');
  ok(-d '/opt/nagios/var/rw', 'nagios runtime dir');
  $output = `/bin/ls -ld /opt/nagios/var/rw 2>&1`;
  like($output, qr/^......s/, 'runtime dir sticky bit set');
  ok(-f '/etc/httpd/conf.d/nagios.conf', 'nagios web conf');
  ok(-f '/opt/nagios/etc/htpasswd.users', 'nagios password created');
  ok(-f '/opt/nagios/etc/nagios.cfg', 'nagios configuration created');
  $output = `rocks dump nagios 2>&1`;
  like($output, qr/administrators/, 'nagios default contact defined');
  ok(-f '/opt/nagios/.ssh/id_rsa', 'nagios ssh key created');
  chomp($output = `/bin/ls -ld /opt/nagios 2>&1 | awk ' {print \$3}'`);
  is($output, 'nagios', '/opt/nagios ownership set');
  chomp($output = `/bin/ls -ld /opt/nagios 2>&1 | awk ' {print \$4}'`);
  is($output, 'apache', '/opt/nagios group set');

}

# nsca-client.xml
ok(-f '/opt/nagios/bin/nsca', 'nsca installed');
ok(-f '/opt/nagios/libexec/check_dummy', 'nagios plugins installed');
`grep -q '^nagios:' /etc/group 2>&1`;
ok($? == 0, 'nagios group defined');
$output = `id nagios 2>&1`;
ok($? == 0, 'nagios login defined');
like($output, qr/uid=413/, 'nagios uid');
$output = `/bin/ls -ld /opt/nagios/etc 2>&1`;
like($output, qr/nagios\s*apache/, '/opt/nagios/etc created');
ok(-f '/opt/nagios/etc/send_nsca.cfg', 'nsca config installed');
ok(-f '/opt/nagios/bin/nsca_schedule', 'nsca_schedule installed');
ok(-f '/opt/nagios/bin/nsca_check', 'nsca_check installed');

# nsca-server.xml
SKIP: {
  skip 'not server', 2 if $appliance ne 'Frontend';
  ok(-f '/opt/nagios/bin/nsca', 'nsca installed');
  ok(-f '/opt/nagios/etc/nsca.cfg', 'nsca config installed');
  `grep -q '^nsca' /etc/services 2>&1`;
  ok($? == 0, 'nsca added to /etc/services');
  ok(-f '/etc/xinetd.d/nsca', 'nsca daemon installed');
  $output = `/bin/ls -ld /opt/nagios 2>&1`;
  like($output, qr/nagios\s*apache/, '/opt/nagios ownership set');
  $output = `rocks list attr | grep NSCA_ServerName`;
  like($output, qr/NSCA_ServerName/, 'nsca attr set');
}
