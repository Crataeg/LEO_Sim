@echo off
"D:\Matlab\bin\win64\MATLAB.exe" -nosplash -nodesktop -logfile "W:\matlab_bat_log.txt" -r "try, run(''W:/matlab_smoke_script.m''); catch ME, disp(getReport(ME,''extended'')); end; exit;"
