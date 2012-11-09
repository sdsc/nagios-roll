# default: on
# description: NSCA (Nagios Service Check Acceptor)
service nsca
{
        flags           = REUSE
        socket_type     = stream
        wait            = no
        user            = nagios
        group           = apache
        server          = /opt/nagios/bin/nsca
        server_args     = -c /opt/nagios/etc/nsca.cfg --inetd
        log_on_failure  += USERID
        disable         = no
        only_from       = NSCA_SERVER_ADDR/NSCA_SERVER_NETMASKBITS
        cps             = 400 10
}
