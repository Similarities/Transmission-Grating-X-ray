# Transmission-Grating-X-ray
image processing for calibration

Laser plasma sources can generate incoherent soft-xray radiation in a wide spectral range (50-1500 eV).
Xrays are diffracted with using a transmission grating (10000 lines/mm) and the spectrum is recorded with a CCD. As in this wide range the CCD cannot record the full spectral range, the detection angle (and with the CCD) has to be changed. In order to characterise the Laser plasma source in this wide range, different measurements at different
spectral ranges have to be patched. In this experiment the CCD was mounted in a vaccuum compatible rotation stage, although the rotation axis had some mismatch with the grating position. All of this has to be corrected in the grating equation. The resulting grating equation takes into account different sources of systematic deviations: as increasing difference of the detection angle with the angle (which is a consequence of the mismatched rotation axis e.g.) and others. 

- The recorded spectrum needs to be integrated (line out) - background substracted, maybe rotated - or flipped, normalized to 1/s for longer or shorter exposuring times 
- px- range in x has to be calculated to spectral range (grating equation usually in wavelength nm)
- the retrieved spectrum needs to be stitched together for different detection angles
- some control data (emission lines, soft-x-ray filter edges) are overlayed in the plot in order to validate the used grating equation.
- in the last step, the transmission values of the filters, the CCD efficiency, the grating efficiency and so on, can be known within a certain uncertainity, this can be used to approximate the emission of the source in terms of photon-nmbers per second and within a certain detection angle (given in steradian).

