# facebook-comment-scraper
A Selenium-based Python script that scrapes comments from Facebook posts. It can
be used stand-alone or in conjuction with services such as [CrowdTangle]
(https://www.crowdtangle.com).

The script requires Selenium with ChromeDriver. This module, along with other
dependencies, should be put in a virtual environment. 

A VPN with several local relays (corresponding geographically to the Facebook
group(s)) is highly recommended. Measures have been taken to avoid blocking, but
only to forestall the inevitable: Blocking *will* happen given sufficiently long
runs. Guaranteed.

## Installation

1. Download the script and install the dependencies.
2. Prepare a plain text list of URLs of Facebook posts on the following form:

`https://m.facebook.com/<GROUP ID>/posts/<POST ID>`

Note that the URLs must point to the mobile version of Facebook, as this is the
only version with which the script is compatible.

3. Run the script from the command line:

`./scraper.py`
