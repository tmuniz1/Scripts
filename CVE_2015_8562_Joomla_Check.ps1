###############################################################################################
#
# Script: CVE_2015_8562_Joomla_Check.ps1
# By: Tim Muniz
# Date: 20151222
#
###############################################################################################
<#

.SYNOPSIS

This script checks Joomla Version to check if the remote host is vulnerable to CVE-2015-8562.



.DESCRIPTION

This script checks Joomla Version to check if the remote host is vulnerable to CVE-2015-8562.


.PARAMETER target

a host running Joomla to test.



.PARAMETER Https

To test a host running SSL/TLS. 

This is an optional parameter.



.EXAMPLE

Check remote Joomla Host and report if vulnerable.

CVE_2015_8562_Joomla_Check.ps1 myjoomla.com 



.EXAMPLE 

Check remote Joomla Host running SSL/TLS and report if vulnerable.

CVE_2015_8562_Joomla_Check.ps1 myjoomla.com -Https



.NOTES

Please let me know what you think or if it isn't working. Also, it relies on access to /language/en-GB/en-GB.xml

#>
[CmdletBinding()]
Param(
  
  
    [Parameter(Mandatory=$True,Position=1)]
    [string] $target,
    
    [Switch]$Https = $false    

)
    
if ($Https){
    write-host "Checking host: $target"
    $site = Invoke-WebRequest -Uri https://$target/joomla/language/en-GB/en-GB.xml -UseBasicParsing
 $xml = [xml]$site.Content
 $version = $xml.metafile.version[1]
    if($version -notlike "3.4.[6-7]"){
        write-host "Your Instance of Joomla is VULNERABLE!"
        write-host "Please Upgrade to 3.4.6."
        write-host "Joomla host is running version " $version
    }
    else { 
        write-host "You are running the updated version of Joomla"
        write-host "Joomla host is running version " $version
    }
}
else {
    write-host "Checking host: $target"
    $site = Invoke-WebRequest -UseBasicParsing -Uri http://$target/joomla/language/en-GB/en-GB.xml
 $xml = [xml]$site.Content
 $version = $xml.metafile.version[1]
    if($version -notlike "3.4.[6-7]"){
        write-host "Your Instance of Joomla is VULNERABLE!"
        write-host "Please Upgrade to 3.4.6."
        write-host "Joomla host is running version " $version
    }
    else { 
        write-host "You are running the updated version of Joomla"
        write-host "Joomla host is running version " $version
    }
}
