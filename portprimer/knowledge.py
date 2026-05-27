from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortKnowledge:
    port: int
    service: str
    learning_label: str
    action_hint: str
    what_it_is: str
    why_it_matters: str
    beginner_note: str
    purpose: str = ""
    used_for: str = ""
    common_misuse_or_attack: str = ""
    should_it_be_open: str = ""
    beginner_takeaway: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "purpose", self.purpose or self.what_it_is)
        object.__setattr__(self, "used_for", self.used_for or self.what_it_is)
        object.__setattr__(self, "common_misuse_or_attack", self.common_misuse_or_attack or self.why_it_matters)
        object.__setattr__(self, "should_it_be_open", self.should_it_be_open or self.action_hint)
        object.__setattr__(self, "beginner_takeaway", self.beginner_takeaway or self.beginner_note)


UNKNOWN_KNOWLEDGE = PortKnowledge(
    port=0,
    service="Unknown service",
    learning_label="Unknown Door",
    action_hint="Learn more before changing",
    what_it_is="This port is open, but PortPrimer does not have a common-service note for it.",
    why_it_matters="Unknown services are worth identifying before you decide whether they are expected.",
    beginner_note="Check the application or system documentation before changing anything.",
)


PORT_KNOWLEDGE: dict[int, PortKnowledge] = {
    20: PortKnowledge(20, "FTP Data", "Legacy Door", "Replace or disable if unused", "FTP data ports move file contents for older FTP transfers.", "Plain FTP is older and can expose data if it is not protected another way.", "Prefer modern protected file transfer when you can."),
    21: PortKnowledge(21, "FTP", "Legacy Door", "Replace or disable if unused", "FTP is used to transfer files between systems.", "Classic FTP does not protect usernames, passwords, or files by itself.", "If FTP is open, confirm it is needed and limited to trusted users."),
    22: PortKnowledge(22, "SSH", "Admin Door", "Keep private", "SSH is used to remotely manage a machine.", "It is normal on servers, but admin access should be protected carefully.", "If SSH is open, use strong authentication and restrict who can reach it."),
    23: PortKnowledge(23, "Telnet", "Legacy Door", "Replace or disable if unused", "Telnet is an old remote login service.", "It sends traffic without modern protection and is rarely appropriate today.", "If you find Telnet, look for a safer replacement such as SSH."),
    25: PortKnowledge(25, "SMTP", "Mail Door", "Review if unexpected", "SMTP is used to send mail between mail servers.", "Mail services need careful configuration to avoid abuse and delivery problems.", "If this is not a mail server, SMTP is usually unexpected."),
    53: PortKnowledge(53, "DNS", "Name Door", "Review if unexpected", "DNS translates names into network addresses.", "Open DNS can be normal for resolvers or name servers, but exposure should match the role.", "Confirm whether the system is supposed to answer DNS queries."),
    67: PortKnowledge(67, "DHCP Server", "System Door", "Keep private", "DHCP servers hand out network settings to clients.", "Unexpected DHCP servers can confuse local networks.", "DHCP usually belongs on trusted local networks only."),
    68: PortKnowledge(68, "DHCP Client", "System Door", "Usually okay if expected", "DHCP clients receive network settings from a server.", "This is common on client machines and lab systems.", "Seeing DHCP is usually a network configuration clue, not a problem by itself."),
    80: PortKnowledge(80, "HTTP", "Web Door", "Usually okay if expected", "HTTP serves websites or web applications without built-in encryption.", "Web services are common, but public exposure should be intentional.", "If HTTP is open, learn what site or app is being served."),
    110: PortKnowledge(110, "POP3", "Mail Door", "Replace or disable if unused", "POP3 lets mail clients retrieve email.", "Older mail retrieval can expose sensitive access if not protected.", "Prefer protected mail settings when email services are needed."),
    111: PortKnowledge(111, "RPCbind", "System Door", "Keep private", "RPCbind helps some Unix services find RPC program ports.", "It is usually a backend system service and should not be widely exposed.", "If open, check which local services require it."),
    123: PortKnowledge(123, "NTP", "System Door", "Review if unexpected", "NTP keeps system clocks synchronized.", "Accurate time matters for logs, authentication, and certificates.", "Use trusted time sources and avoid exposing time services unnecessarily."),
    135: PortKnowledge(135, "Microsoft RPC", "System Door", "Keep private", "Microsoft RPC supports Windows service communication.", "It is common in Windows environments but should usually stay on trusted networks.", "If exposed, confirm the network boundary is appropriate."),
    139: PortKnowledge(139, "NetBIOS", "Private Door", "Keep private", "NetBIOS supports older Windows file and name sharing.", "It is generally intended for local trusted networks.", "Avoid exposing NetBIOS outside your private network."),
    143: PortKnowledge(143, "IMAP", "Mail Door", "Replace or disable if unused", "IMAP lets mail clients read and manage email on a server.", "Mail access should be protected because accounts contain sensitive data.", "Prefer protected IMAP settings and strong account security."),
    161: PortKnowledge(161, "SNMP", "System Door", "Keep private", "SNMP is used to monitor and manage network devices.", "It can reveal useful system details when misconfigured.", "Keep SNMP private and use strong modern settings."),
    389: PortKnowledge(389, "LDAP", "System Door", "Keep private", "LDAP provides directory information such as users and groups.", "Directory services are sensitive and should match the network trust boundary.", "If LDAP is open, confirm who needs to query it."),
    443: PortKnowledge(443, "HTTPS", "Web Door", "Usually okay if expected", "HTTPS serves encrypted websites or web applications.", "It is common for public web apps, but the app still needs secure configuration.", "If HTTPS is open, identify the application and keep it patched."),
    445: PortKnowledge(445, "SMB", "Private Door", "Keep private", "SMB is commonly used for Windows file sharing.", "File sharing can expose sensitive data if reachable by the wrong people.", "SMB should usually stay on trusted private networks."),
    465: PortKnowledge(465, "SMTPS", "Mail Door", "Review if unexpected", "SMTPS is encrypted SMTP used by some mail setups.", "Mail services require careful authentication and relay settings.", "If this is not a mail system, investigate why it is open."),
    512: PortKnowledge(512, "rexec", "Legacy Door", "Lab only", "rexec is an old remote command service.", "It is mostly seen in legacy systems or training labs.", "Treat rexec as a lab-only learning signal unless you know it is required."),
    513: PortKnowledge(513, "rlogin", "Legacy Door", "Lab only", "rlogin is an old remote login service.", "It lacks the protections expected from modern remote access.", "Use it only in isolated labs built for learning."),
    514: PortKnowledge(514, "rsh/syslog", "Legacy Door", "Lab only", "Port 514 may be old remote shell or syslog traffic.", "Remote shell use is legacy, while syslog should be designed carefully.", "Identify which service is present before making changes."),
    587: PortKnowledge(587, "SMTP Submission", "Mail Door", "Review if unexpected", "SMTP submission is used by mail clients to send outbound email.", "It should require authentication and protected settings.", "If open, confirm it is part of an intended mail service."),
    993: PortKnowledge(993, "IMAPS", "Mail Door", "Usually okay if expected", "IMAPS is encrypted IMAP for reading email.", "Mail access still depends on good authentication and account security.", "If expected, keep mail software patched and accounts protected."),
    995: PortKnowledge(995, "POP3S", "Mail Door", "Usually okay if expected", "POP3S is encrypted POP3 for retrieving email.", "It protects transport better than plain POP3 but still needs secure accounts.", "If used, confirm old accounts and weak passwords are not lingering."),
    1099: PortKnowledge(1099, "Java RMI", "System Door", "Keep private", "Java RMI lets Java applications communicate remotely.", "It is usually an internal application service.", "Keep RMI on trusted networks unless there is a clear design reason."),
    1433: PortKnowledge(1433, "Microsoft SQL Server", "Data Door", "Keep private", "Microsoft SQL Server stores and serves database data.", "Databases often contain sensitive records and should be tightly limited.", "Database ports should normally be reachable only by trusted application hosts."),
    1521: PortKnowledge(1521, "Oracle Database", "Data Door", "Keep private", "Oracle Database stores and serves structured data.", "Database exposure should be intentional and strongly controlled.", "Keep database access private unless your architecture clearly requires otherwise."),
    1524: PortKnowledge(1524, "Metasploitable shell service", "Lab Door", "Lab only", "This is a known lab service on Metasploitable 2.", "It exists for training and should not appear on normal systems.", "Use this only inside an isolated local lab VM."),
    2049: PortKnowledge(2049, "NFS", "Private Door", "Keep private", "NFS shares files between Unix-like systems.", "File shares can expose data if permissions or network reach are too broad.", "Keep NFS limited to trusted hosts that need it."),
    2121: PortKnowledge(2121, "FTP Alternate", "Legacy Door", "Lab only", "Port 2121 is often used as an alternate FTP service in labs.", "Alternate ports can hide old services from quick checks.", "Confirm what application owns the port before changing it."),
    2375: PortKnowledge(2375, "Docker API", "Admin Door", "Keep private", "Docker API can manage containers on a host.", "Unprotected container management access is very sensitive.", "Keep Docker management interfaces private and protected."),
    3000: PortKnowledge(3000, "Development Server", "Web Door", "Review if unexpected", "Port 3000 often hosts development web applications.", "Dev servers may not be configured for public exposure.", "Use it for local development unless you intentionally deployed it."),
    3306: PortKnowledge(3306, "MySQL", "Data Door", "Keep private", "MySQL stores and serves database data.", "Database services should be reachable only by systems that need them.", "If MySQL is open, confirm it is not exposed beyond trusted networks."),
    3389: PortKnowledge(3389, "RDP", "Admin Door", "Keep private", "RDP is used to remotely access Windows desktops.", "Remote desktop access should be strongly protected and limited.", "If RDP is open, restrict reachability and use strong authentication."),
    5432: PortKnowledge(5432, "PostgreSQL", "Data Door", "Keep private", "PostgreSQL stores and serves database data.", "Databases often hold important application information.", "Keep PostgreSQL private to trusted application systems."),
    5900: PortKnowledge(5900, "VNC", "Admin Door", "Keep private", "VNC provides remote graphical desktop access.", "Remote desktop tools need careful access control.", "Avoid exposing VNC outside a trusted local or VPN network."),
    6000: PortKnowledge(6000, "X11", "Legacy Door", "Keep private", "X11 supports graphical display connections on Unix-like systems.", "Remote display services are rarely meant for broad exposure.", "If X11 is open, verify whether remote display access is actually needed."),
    6379: PortKnowledge(6379, "Redis", "Data Door", "Keep private", "Redis is an in-memory data store often used by applications.", "It can contain sensitive application data or control queues.", "Redis should usually listen only on private interfaces."),
    6667: PortKnowledge(6667, "IRC", "Lab Door", "Lab only", "IRC is a chat protocol and appears in some security labs.", "On lab VMs it may exist for practice scenarios.", "If this is not a lab, identify why chat service traffic is present."),
    8000: PortKnowledge(8000, "Development Web Server", "Web Door", "Review if unexpected", "Port 8000 often hosts development or alternate web services.", "Development services may expose test pages or admin tools.", "Confirm whether this web service is meant to be reachable."),
    8009: PortKnowledge(8009, "AJP", "System Door", "Keep private", "AJP connects web servers to Java application servers.", "It is usually backend plumbing, not a public-facing service.", "Keep AJP private between trusted web and app servers."),
    8080: PortKnowledge(8080, "HTTP Alternate", "Web Door", "Review if unexpected", "Port 8080 commonly hosts alternate web applications or proxies. In Playground Tour, it is only a safe local practice service created by PortPrimer.", "It is easy to forget test or admin web apps on alternate ports. Playground Tour does not implement real HTTP or a vulnerable service.", "For real systems, inspect the service only when you are authorized. In Playground Tour, this exists so you can see how open ports appear in a scan."),
    8180: PortKnowledge(8180, "Alternate Web App", "Web Door", "Review if unexpected", "Port 8180 often hosts alternate web application consoles.", "Admin or test applications on alternate ports still need protection.", "Identify the application and confirm it is expected."),
    8022: PortKnowledge(8022, "Playground SSH-style service", "Admin Door", "Lab only", "This is a safe local practice service created by PortPrimer.", "It is not a real SSH service or a vulnerable service. It exists so you can see how an admin-style open port appears in a scan.", "Playground services bind only to 127.0.0.1 and are for local learning only."),
    15432: PortKnowledge(15432, "Playground Database-style service", "Data Door", "Lab only", "This is a safe local practice service created by PortPrimer.", "It is not a real database or a vulnerable service. It exists so you can see how a data-style open port appears in a scan.", "Playground services bind only to 127.0.0.1 and are for local learning only."),
    16379: PortKnowledge(16379, "Playground Cache-style service", "Data Door", "Lab only", "This is a safe local practice service created by PortPrimer.", "It is not Redis, a real cache, or a vulnerable service. It exists so you can see how a cache-style open port appears in a scan.", "Playground services bind only to 127.0.0.1 and are for local learning only."),
    18080: PortKnowledge(18080, "Playground Web-style service", "Web Door", "Lab only", "This is a safe local practice service created by PortPrimer.", "It is not a real web service or a vulnerable service. It exists so you can see how a web-style open port appears in a scan.", "Playground services bind only to 127.0.0.1 and are for local learning only."),
    8443: PortKnowledge(8443, "HTTPS Alternate", "Web Door", "Review if unexpected", "Port 8443 commonly hosts encrypted alternate web services.", "It may be an admin console, test app, or secondary web service.", "If open, learn which app owns it and who should reach it."),
    9200: PortKnowledge(9200, "Elasticsearch", "Data Door", "Keep private", "Elasticsearch stores and searches indexed data.", "Search indexes can contain sensitive application records.", "Keep Elasticsearch private unless it is deliberately protected."),
    27017: PortKnowledge(27017, "MongoDB", "Data Door", "Keep private", "MongoDB stores document-oriented database data.", "Database exposure can matter a lot depending on data and access controls.", "Keep MongoDB reachable only by trusted systems."),
}


def get_port_knowledge(port: int) -> PortKnowledge:
    known = PORT_KNOWLEDGE.get(port)
    if known:
        return known
    return PortKnowledge(
        port=port,
        service=UNKNOWN_KNOWLEDGE.service,
        learning_label=UNKNOWN_KNOWLEDGE.learning_label,
        action_hint=UNKNOWN_KNOWLEDGE.action_hint,
        what_it_is=UNKNOWN_KNOWLEDGE.what_it_is,
        why_it_matters=UNKNOWN_KNOWLEDGE.why_it_matters,
        beginner_note=UNKNOWN_KNOWLEDGE.beginner_note,
    )
