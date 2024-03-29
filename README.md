# HoneyCheck - Detect Rogue DHCP Servers in your network

![Honeycheck logo](assets/honeycheck_horizontal.png)

Honeycheck detects rogue DHCP servers and provides a modular and fully
configurable action environment in case they are found.

### Doc Index

- [System requirements](#system-requirements)
- [Honeycheck installaton](#honeycheck-installation)
- [Configuring honeycheck](#configuring-honeycheck)
- [Running honeycheck](#running-honeycheck)
- [Extending honeycheck](#extending-honeycheck)
- [Donations and Sponsorships](#donations-and-sponsorships)


## System requirements

```bash
apt-get install -y python3 virtualenv bridge-utils tcpdump
```

## Honeycheck Installation

```bash
pip install honeycheck
```

## Configuring Honeycheck

Honeycheck requires a configuration file as a parameter.

The interfaces on which it will work must be indicated in the configuration
file.

For each interface, you must define which control module will be executed when
a malicious `fail_test` server is detected or when it apparently stops being
detected pass_test.

Control objects are highly customizable pieces of software. Each module
receives parameters that must be configured.

The control object `honeycheck.modules.script.Script` allows the execution of
scripts and receives the script to execute as a parameter.

Depending on the check, the parameter will be prefixed with `fail_test`,
`pass_test` or `final_exec`.

- fail_test will be executed if a rogue DHCP server is detected
- pass_test will be executed if a rogue DHCP seems to be removed from the network
> pass_test can through false_negatives if the rogue_dhcp response are not detected
  in a period of time.
- final_exec will be executed after each check

The configuration file must be created before running honeycheck.

### Configuration sample

> Note that honeycheck can work in multiple network interfaces at the same time.


```ini
[wlp0s20f3] # Configuration for wlp0s20f3 network interface
	# Less than 30 seconds can give flapping false negatives
	discover_timeout = 30
	
	# test syntax: module.ControlClass
	fail_test =    honeycheck.modules.script.Script
	fail_test_script_path = scripts/zenity_fail.sh

	pass_test = honeycheck.modules.script.Script
	pass_test_script_path = scripts/zenity_pass.sh

	pass_test = honeycheck.modules.script.Script
	pass_test_script_path = /my/custom/script

[eth0]
	discover_timeout = 30
	fail_test =    honeycheck.modules.script.Script
	fail_test_script_path = scripts/zenity_fail.sh

```

## Running Honeycheck

Once Honeycheck is configured it can be started running `python3 -m honeycheck
-c our_conf_file.cnf`

## Extending Honeycheck

You can create your own modules to configure the behavior of honeycheck.

To do this all you have to do is inherit from the BaseControl abstract class located in `honeycheck.modules.base_control`.

### Example of a Custom Control Object

```python
from honeycheck.modules.base_control import BaseControl, ControlConfigurationReq


class MyCustomControlObject(BaseControl):
    def apply_actions(self, dhcp_watcher, **kwargs):
        servers = dhcp_watcher.dhcp_servers
        whitelist = dhcp_watcher.whitelist

        # Retrieve a param value from configuration
        script_path = self._conf.get_req("script_path")

        # Do your stuff here...
        # Send an email, open an issue, publish a message to rabbitmq. whatever
        # you want.


    def get_conf_req(self) -> ControlConfigurationReq:
        # Return a ControlConfigurationReq object with the required
        # configuration this control object needs
        return ControlConfigurationReq(["script_path"])
```

Once you have created your custom control object you will need to add it to
your system as a python package.

After this you will be able to select it in the honeycheck configuration. 
`fail_test = mycustom_module.MyCustomControlObject`


## Donations and Sponsorships

![Donations](assets/donations.png)

### Donations from people/companies

If this tool is useful to you, please consider making a donation to support my
work.

Donations allow me to continue developing open source software to contribute
and grow our community.

I wish some day I could focus only on creating quality open source with a
strong community
supporting my projects.

You support me on https://ko-fi.com/elchicodepython.

### Sponsorships

If your company uses this tool and would like it to have a specific feature,
your company can sponsor its development.

To sponsor the development of a feature [contact
me](https://es.linkedin.com/in/sam-sec).

### Product integration advertising

If you want the integration of this tool with your solution to appear in this
Readme, [contact me](https://es.linkedin.com/in/sam-sec).
