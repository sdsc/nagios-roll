# SDSC "nagios" roll

## Overview

This roll bundles the Nagios cluster monitoring package.

For more information about the various packages included in the nagios roll please visit their official web pages:

- <a href="http://www.nagios.org" target="_blank">Nagios</a> is a powerful
monitoring system that enables organizations to identify and resolve IT
infrastructure problems before they affect critical business processes.
- <a
href="http://exchange.nagios.org/directory/Addons/Passive-Checks/NSCA--2D-Nagios
-Service-Check-Acceptor/details" target="_blank">NSCA</a>, the Nagios Service
Check Acceptor is a Linux/Unix daemon allows you to integrate passive alerts and
checks from remote machines and applications with Nagios.


## Requirements

To build/install this roll you must have root access to a Rocks development
machine (e.g., a frontend or development appliance).

If your Rocks development machine does *not* have Internet access you must
download the appropriate nagios source file(s) using a machine that does
have Internet access and copy them into the `src/<package>` directories on your
Rocks development machine.


## Dependencies

The sdsc-roll must be installed on the build machine, since the build process
depends on make include files provided by that roll.


## Building

To build the nagios-roll, execute this on a Rocks development
machine (e.g., a frontend or development appliance):

```shell
% make 2>&1 | tee build.log
```

A successful build will create the file `weka-*.disk1.iso`.  If you built the
roll on a Rocks frontend, proceed to the installation step. If you built the
roll on a Rocks development appliance, you need to copy the roll to your Rocks
frontend before continuing with installation.


## Installation

To install, execute these instructions on a Rocks frontend:

```shell
% rocks add roll *.iso
% rocks enable roll nagios
% cd /export/rocks/install
% rocks create distro
% rocks run roll nagios | bash
```


## Testing

The nagios-roll includes a test script which can be run to verify proper
installation of the roll documentation, binaries and module files. To
run the test scripts execute the following command(s):

```shell
% /root/rolltests/nagios.t 
```
