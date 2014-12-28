email-backup
=

A set of simple scripts to manage email backup for any server supporting `IMAP v4`. These scripts are designed to run periodically as services.

To use with **Gmail**, you will need to setup an [**application specific password**](https://support.google.com/mail/answer/1173270?hl=en).

Quickstart
=

* Checkout repo.
* Requires Python (tested on 2.7.6).
* Requires `imaplib`, `email`, and `zipfile` among other Python libs. Usually these are installed by default.
* Run `python ebackup.py -o . -e YOUR_EMAIL -p YOUR_PASSWORD -i IMAP_SERVER`.
	* For Gmail users:
		* Create an [**application specific password**](https://support.google.com/mail/answer/1173270?hl=en).
		* `IMAP_SERVER` will be imap.gmail.com.
* Once the command finishes, you should see a directory named `YOUR_EMAIL` in the current directory. This is your archive.

Motivation
=

**I wanted something simple**. I'm a crotchety old man in software-engineer years. I don't want hardware, I don't want to pay, I don't want a web service, I don't want an app for my phone-- I want a few hundred lines of easy-to-read, easy-to-debug code.

This particular solution can be easily used in tandem with pretty much any existing backup. I use a local external backup drive and SpiderOak for remote backup (zero-knowledge remote backup is, I think, a pretty big deal). Version control integration would also be trivial.

Overview
=

There are three main scripts:

`ebackup.py` downloads a copy of new messages into a simple folder hierarchy with flat files.

`ebarchiver.py` updates a zip archive with new messages. 

`ebexporter.py` can be used to create a single `.mbox` file from this folder structure. This is useful for reimporting a mailbox.

ebackup.py
=

`ebackup` supports any host with `IMAPv4` access.

![Usage](images/ebackupUsage.png)

The script will download only new messages by keeping track locally of which messages it has already downloaded. It does not use IMAP `FLAGS`.

Each message will be written to a distinct flat file. The directory structure is `[year]/[month]/[day]/[hour].[minute].[second]_[id].message`.

![Hierarchy](images/ebackupHierarchy.png)

ebarchiver.py
=

`ebarchiver` is used to intelligently create and maintain a `zip` archive of emails.

![Usage](images/ebarchiverUsage.png)

The archiver acts on the root directory of `ebackup` output, and maintains an up to date `zip` archive.

Due to the static nature of the `zip` format, this script keeps an external database of emails that exist inside of an archive. 

ebexporter.py
=

`ebexporter` is useful for compiling all emails into a single `.mbox` file.

![Usage](images/ebexporterUsage.png)

The exporter accepts a directory output from `ebackup`, and compiles the messages into an ordered `Mailbox` file.

How to install as scheduled task on Windows
=

These scripts should be run periodically. On Linux and Unix, users can set up scheduled tasks in a variety of ways. On Windows, you can use **Scheduled Tasks**.

**1.** Open Task Scheduler.

![Task Scheduler](images/TaskScheduler.png)

**2.** Copy `ebtask_example.bat` to `ebtask.bat` (which is already ignored by the `.gitignore`).

**3.** Fill in various variables.

![BAT](images/TaskBat.png)

**4.** In Task Scheduler, schedule `ebtask.bat` to run on whatever schedule you choose.

But why doesn't...
=

**...`ebackup` just add new messages to a single `mbox` file to begin with?** Because a giant `mbox` file is harder to work with. You would have to parse the whole file to do simple queries (where are my emails from December?). You could not peruse and open messages easily. Because this is simpler.

**...`ebackup` use `FLAGS`?** `FLAGS` are not something my little python script has complete control over.

**...`ebarchiver` internally keep track of which emails are inside of the archive?** I would love to have the db index inside of the archive (and I originally wrote it that way), but the entire `zip` archive would need to be rewritten every time a new message was added. This is because archived files may not be updated once deflated. As the archive grew over time, the execution time would as well. I tested this on a ~7 GB archive and the execution time was far too high for my taste.

**...something else?** If you have a suggestion, I'd love to hear it.