for /L %%i in (1,1,10) do (

	echo %%i

	waitfor SomethingThatIsNeverHappening /t 1 2>NUL || type nul>nul
)
pause