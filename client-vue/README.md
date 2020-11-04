## DSS Monitor and Control client v1.4.3

DSS Monitor Control client built with Vue.js.

### Prepare

Presumably you have already cloned this repo in some directory on your local host.

Install `npm`.

### Build

Currently using webpack v4 for build.

```
npm init
npm install
npm run build:prod
```

### Test

```
npm run test
```

### Use

The client works through a server using socket port 5000.  

1. If you run the server
   locally (located in `DSN-Sci-packages/MonitorControl/apps/server/web_server.py`)
   then you can just start your client (step 4).

2. If the server is running on an accessible network, then create a tunnel to the
   server with<br/>
   ```
   ssh -N -L 5000:serverhost:5000 serverhost -l ${USER} > /dev/null 2>&1
   ```

3. If the server is running on a firewalled network, the first create a tunnel to
   the remote host, and then a tunnel to the host's port 5000.  For example,<br/>
   ```
   ssh-tunnel dto;
   ssh -N -L 5000:localhost:5000 localhost -p 50021 -l ${USER} > /dev/null 2>&1
   ```<br/>
   where 50021 is the prot for the tunnel to `dto`.

4. With the server running, and any necessary tunnels in place, simply open
   `index.html` (in this directory) in your favorite (Firefox) browser.
