# Constellation Data Integration Note

Current step:
- Downloaded open GP/TLE data from the official CelesTrak interface.
- Generated an initial shell distribution plot using Starlink and OneWeb current orbital data.

Why this matters for the IEICE direction:
- It turns the platform from a purely self-defined simulation scene into a data-informed scenario.
- It enables figures based on real constellation shells, not only synthetic 12x8 orbital settings.
- It supports later additions such as visible-satellite counts over Qingdao/Beijing, access windows, and constellation-aware interference cases.

Current limitations:
- The present plot only uses GP-derived orbital elements, not high-precision ephemeris propagation.
- Gateway and beam data are not yet included.
- The current platform logic is still synthetic and has not yet been coupled to these real shells.

Next recommended step:
- Replace the fixed 12x8 shell in one branch of the engineering code with a Starlink/OneWeb subset built from open GP data.
