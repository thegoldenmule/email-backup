set PYTHON=C:\Python27\python.exe
set BASE_DIR=[Your email-backup checkout]
set OUTPUT_DIR=[Directory to output archive]

set EMAIL=[Email address]
set PASSWORD=[Password (application specific password for gmail accounts)]
set IMAP=[IMAP server address]

%python% %BASE_DIR%\ebackup.py -e %EMAIL% -p %PASSWORD% -i %IMAP% -o %OUTPUT_DIR%
%python% %BASE_DIR%\ebexporter.py -i %OUTPUT_DIR%\%EMAIL% -o %OUTPUT_DIR%\%EMAIL%\Archive.mbox