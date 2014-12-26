@echo off set PYTHON=C:\Python27\python.exe
@echo off set BASE_DIR=[Your email-backup checkout]
@echo off set OUTPUT_DIR=[Directory to output archive]

@echo off set EMAIL=[Email address]
@echo off set PASSWORD=[Password (application specific password for gmail accounts)]
@echo off set IMAP=[IMAP server address]
%python% %BASE_DIR%\ebackup.py -e %EMAIL% -p %PASSWORD% -i %IMAP% -o %OUTPUT_DIR%
%python% %BASE_DIR%\ebexporter.py -i %OUTPUT_DIR%\%EMAIL% -o %OUTPUT_DIR%\Archive.mbox