set PYTHON=C:\Python27\python.exe
set BASE_DIR=[Your email-backup checkout]
set OUTPUT_DIR=[Directory to output archive]

set EMAIL=[Email address]
set PASSWORD=[Password (application specific password for gmail accounts)]
set IMAP=[IMAP server address]

%python% %BASE_DIR%\ebackup.py -e %EMAIL% -p %PASSWORD% -i %IMAP% -o %OUTPUT_DIR%\Git
%python% %BASE_DIR%\ebarchiver.py -i %OUTPUT_DIR%\Git\%EMAIL% -o %OUTPUT_DIR%\Archives\%EMAIL%.zip