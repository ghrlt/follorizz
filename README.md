# FolloRizz

### Usage
You can use this program in different ways.
You can either provide credentials in the command arguments:
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
`python3 main.py --username gahrlt --password p4s5w0rd`

or use environnement variables, global or local:
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
`python3 main.py --env /path/to/your/env.file`

<br>
For following uses, while session is valid, you can omit providing password, username is still necessary.

### 2FA Support
If you don't have 2fa already enabled on your online accounts, please do!
Then, this program support account secured with 2fa. You can either:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
- Provide nothing, the program will ask for the 2FA code and handle everything next.
- Provide your 2FA seed. This program will, if needed, generate the 2FA code with your seed and then login.

### Notes
⚠️ I recommend using local environnement file to feed the program with your credentials. This will avoid you leaking your credentials on your OS command history.