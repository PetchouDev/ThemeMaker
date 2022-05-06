::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBZVWAyHAE+1BaAR7ebv/NaErUkYaNY3fYLe97WFJfIv61b3cII+6nNZl8VCBRhXHg==
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSzk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJhZks0
::ZQ05rAF9IBncCkqN+0xwdVsFAlTi
::ZQ05rAF9IAHYFVzEqQIEIB5ZSSmDN26oZg==
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWGmB4EE4Jw5wSRLi
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFBZVWAyHAE+1BaAR7ebv/NaErUkYaNY3fYLe97WFJfIv3k3heJMA13FfioUJFB44
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off & title %~nx0 & color 07

goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
python --version 2>NUL
if errorlevel 1 goto PYTHON_DOES_NOT_EXIST
if errorlevel 0 goto PYTHON_DOES_EXIST
::@pause
goto :EOF

:PYTHON_DOES_NOT_EXIST
echo Python is not installed on your system.
cscript notif.vbs "Can't find Python. Please install it from Microsoft Store and restart the program once done."

@start python
goto :EOF



:PYTHON_DOES_EXIST
:: This will retrieve Python 3.8.0 for example.
for /f "delims=" %%V in ('python -V') do @set ver=%%V
echo Found %ver% on system, checking dependencies
goto :RUN

:RUN
echo check for dependencies
::@pause
python assets\dependencies.py
echo ready for running program
::@pause
python main.py
echo program exit
::@pause

