## Change Log

### v1.0.0

- Moved most styling away from styles.css and into single component files.
This means that each component is really a self contained unit that doesn't
rely on any applicaton-wide styles.css file.
- Moved away from using skeleton grid system, in favor of native css grid.
- Reorganized layout. Antenna monitor and control are much more compact.
Spectrometer calibration is laid out in a much smarter manner, using the
grid instead of a (very) complicated flex box system.

### v1.1.0

- Introduced nodding area (not yet connected to backend)
- css grid is implemented for all components, including flux calibration,
boresight load, boresight run and power meter monitor.
- Introduced __version__ variable into app.js.

### v1.2.0

- Improved the way selecting source flows back to main app.
- App.sourceForObservation now gets a "formatted" field when transmitted to child
components, such that child components don't have to ask parent component to
format the source with the correct color.
- Status bar at the top of the page now displays the currently selected source.
This contrasts with pre v1.0.0 release where there was a bar underneath the
source monitor that showed this information.
- Added version tag at bottom of page

### v1.2.1

- fixed compatibility with new boresight object format from server.
- dropdowns now have a max width. This means they won't enlarge dramatically
as before.

### v1.3.0

- Boresight area now displays the scikit-learn prediction for each boresight
channel.

### v1.4.0

- Connected Nodding component to server-side functionality.

### v1.4.1

- Added Point button.

### v1.4.2

- fixed bug in Offset accept buttons where the buttons weren't using correct event.
- fixed bug where Flux calibration wouldn't tell user what was happening.
- fixed bug where boresight start button didn't work.
- added source info to boresight run

### v1.4.3

- Updated boresight handler functions to reflect server side API change.

### v1.5.0

- Spectrometer control area works.
- Number of roaches displayed corresponds to number of roachs controlled
by server

### v1.5.1

- Status changes when client connects to server.

### v1.5.2

- Now reporting source specific information in the `SourceInfoDisplay` component.

### v1.5.3

- Nodding component can now tell server which source we're nodding on
(independent of the Pointing component)
- Dealing with changes to host computer name changes.
