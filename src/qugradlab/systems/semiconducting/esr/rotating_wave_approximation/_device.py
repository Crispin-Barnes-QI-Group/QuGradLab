"""
Defines a class for storing the parameters for an electron spin resonance
(ESR) device with a linear array of qubits under the rotating wave
approximation.
"""

import numpy as np

class Device():
    """
    A class storing the parameters for an ESR device with a linear array of
    qubits under the rotating wave approximation.
    approximation.
    
    Warning
    -------
    This class does not specify the Hamiltonian model or control scheme.

    See Also
    --------
    * :class:`qugradlab.physical_systems.semiconducting.esr.rotating_wave_approximation._controls.Controls`
    * :class:`qugradlab.physical_systems.semiconducting.esr.rotating_wave_approximation._systems.SpinChain`
    """
    
    _zeeman_detunings: np.ndarray[complex]
    """The Zeeman detunings of adjacent spins"""
    
    _max_drive_strength: float
    """
    The maximum drive strength that can be applied at a specific frequency
    and quadrature. That is if their are ``n_drive_ctrl`` frequencies and both
    quadratures are used then the maximum amplitude of the drive that can be
    applied to the device is::

        np.sqrt(2) * n_drive_ctrl * max_drive_strength
    """
    
    _J_min: float
    """The minimum value of the exchange coupling $J$"""
    
    _J_max: float
    """The maximum value of the exchange coupling $J$"""
    
    def __init__(self,
                 zeeman_detunings: np.ndarray[complex],
                 max_drive_strength: float = 1,
                 J_min: float = 1,
                 J_max: float = 1
                ):
        """Initialises an ESR device with a linear array of qubits under the
        rotating wave approximation.

        Parameters
        ----------
        zeeman_detunings : NDArray[Shape[spins-1], number]
            The Zeeman detunings of the spins
        max_drive_strength : float
            The maximum drive strength that can be applied at a specific
            frequency and quadrature. That is if their are ``n_drive_ctrl``
            frequencies and both quadratures are used then the maximum amplitude
            of the drive that can be applied to the device is::

                np.sqrt(2) * n_drive_ctrl * max_drive_strength
        J_min : float
            The minimum value of the exchange coupling $J$
        J_max : float
            The maximum value of the exchange coupling $J$
        """
        self._zeeman_detunings = np.array(zeeman_detunings)
        self._zeeman_detunings.flags.writeable = False
        self._max_drive_strength = max_drive_strength
        self._J_min = J_min
        self._J_max = J_max

    @property
    def zeeman_detunings(self) -> np.ndarray[complex]:
        """The Zeeman detunings of the spins"""
        return self._zeeman_detunings
    @property
    def max_drive_strength(self) -> float:
        """The maximum drive strength that can be applied to the system"""
        return self._max_drive_strength
    @property
    def J_min(self) -> float:
        """The minimum value of the exchange coupling $J$"""
        return self._J_min
    @property
    def J_max(self) -> float:
        """The maximum value of the exchange coupling $J$"""
        return self._J_max