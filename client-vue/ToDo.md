DSS MonitorControl TODO


### pre v1.4.2

- Track Antenna in SourceMonitor plot [x]
    - I'm not sure how I want to go about this. I could get AntennaMonitor
    to broadcast on global `bus`, or I could get SourceMonitor to track
    Antenna by itself, by making its own server requests. The latter approach
    is more extensible and modular, but harder on resources.
    - I ended up going the former route.
- Increase size of small calibrators [x]
- Show position of source on plot if selected from Source Search area [x]
- Display "onsource" info
    - This is going to be pretty tricky, I think. The `onsource` APC method
    requires a lot of socket time. Maybe I should make it blocking, such that
    no other call can interfere with it? This is a lower level server issue.
- Clear boresight plot after each iteration, or have clear plot button. [x]
    - boresight plot clears when starting fresh boresight iteration
    - I modified clearPlot method in D3StaticPlot component that clears
    lines and paths.
- Revert boresight button to start after boresight is finished. [x]
    - I added a separate toggleDisplay button to StartStopButton component
    that allows toggling display without emitting toggle event.
- Implement minical plot []
- we seem to lose tsys plot after a while.
- can't really do more than one boresight iteration -- sometimes we can't
get boresight results.
    - I suspect that I need to pause timers. Maybe my socket is getting
    saturated?
- incorporate track timing into display []
- implement some sort of message bar, where client can communicate with user [x]
- add SR offsets to Antenna Control area [x]

### v1.5.x

- Not getting source specific information [x]
    - This changed after I changed the way sources were served up to the client.
    Once I took this into account, the situation improved dramatically.
- vertical spacing between elements is ugly in source monitor area [x]
    - I added a bottom margin to panel elements
- Need to find elegant way of incorporating SR offsets into running boresight []
- Hook up spectrometer control area. Only show ROACH row for connected roaches [x]


### v2.0

- use Bulma css framework instead of skeleton for better responsiveness and
generally a better column system.
