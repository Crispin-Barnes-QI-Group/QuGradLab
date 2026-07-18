"""
A collection of :class:`qugrad.QuantumSystem` s for electron spin resonance (ESR)
devices with a linear array of qubits under the rotating wave approximation.
"""

import numpy as np

from ._controls import Controls
from .....hilbert_spaces import QubitSpace
from ....skeletons.qubits import QubitSystem

class SpinChain(Controls, QubitSystem):
    r"""
    A :class:`qugrad.QuantumSystem` for a spin chain with electron spin
    resonance (ESR) controls with a linear array of qubits under the rotating
    wave approximation. The Hamiltonian is given by
    $$
    H(t) = \frac{1}{4} \sum_{i=0}^{\texttt{spins}-1} \left[I_i(t) X_i
    + Q_i(t)Y_i\right]
    + \frac{1}{4} \sum_{i=0}^{\texttt{spins}-2} J_i(t)\left[Z_iZ_{i+1}
    +\cos(\omega_i t)\left[X_iX_{i+1}+Y_iY_{i+1}\right]
    +\sin(\omega_i t)\left[X_iY_{i+1}-Y_iX_{i+1}\right]\right],
    $$
    where
    $X_i$, $Y_i$, and $Z_i$ are the Pauli-x, -y, and -z operators acting on the
    $i$th spin, $\omega_i$ are the Zeeman detunings, $J_i(t)$ is the exchange
    coupling.
    """

    _ferromagnetic: bool
    """Whether the exchange coupling is ferromagnetic or antiferromagnetic"""
    
    def __init__(self,
                 spins: int,
                 zeeman_detunings: np.ndarray[float],
                 max_drive_strength: float,
                 J_max: float,
                 J_min: float = 0,
                 feromagnetic: bool = True,
                 use_graph: bool = True):
        r"""
        Initialises a spin chain with ESR controls. The Hamiltonian is
        given by:
        $$
        H(t) = \frac{1}{4} \sum_{i=0}^{\texttt{spins}-1} \left[I_i(t) X_i
        + Q_i(t)Y_i\right]
        + \frac{1}{4} \sum_{i=0}^{\texttt{spins}-2} J_i(t)\left[Z_iZ_{i+1}
        +\cos(\omega_i t)\left[X_iX_{i+1}+Y_iY_{i+1}\right]
        +\sin(\omega_i t)\left[X_iY_{i+1}-Y_iX_{i+1}\right]\right],
        $$
        where
        $X_i$, $Y_i$, and $Z_i$ are the Pauli-x, -y, and -z operators acting on the
        $i$th spin, $\omega_i$ are the Zeeman detunings, $J_i(t)$ is the exchange
        coupling.
        
        Parameters
        ----------
        spins : int
            The number of spins in the chain
        zeeman_detunings : NDArray[Shape[spins], float]
            The Zeeman detuning of each of the spins
        max_drive_strength : float
            The maximum drive strength that can be applied at a specific
            frequency and quadrature. That is if their are ``n_drive_ctrl``
            frequencies and both quadratures are used then the maximum amplitude
            of the drive that can be applied to the device is::

                np.sqrt(2) * n_drive_ctrl * max_drive_strength
        J_max : float
            The minimum value of the exchange coupling $J$
        J_min : float
            The maximum value of the exchange coupling $J$, by default 0
        feromagnetic : bool
            If ``True``, the exchange coupling is ferromagnetic. If ``False``,
            the exchange coupling is antiferromagnetic. By default, ``True``.
        use_graph : bool
            Whether to use `TensorFlow <https://www.tensorflow.org>`__ graphs
            during computation, by default ``True``
        """
        Controls.__init__(self,
                          zeeman_detunings,
                          max_drive_strength,
                          J_min,
                          J_max)
        single_qubit_drift_coefficients = np.zeros((spins, 3))
            
        single_qubit_ctrl_coefficients = \
            np.stack([np.array([[1/4, 0, 0]]*spins),
                      np.array([[0, 1/4, 0]]*spins)])
        
        forward_connectivity = np.einsum("ij,jk->ijk",
                                         np.eye(spins, spins, 0),
                                         np.eye(spins, spins, 1)
                                        )[:-1]
        backward_connectivity = np.einsum("ij,jk->ijk",
                                          np.eye(spins, spins, 1),
                                          np.eye(spins, spins, -1)
                                         )[:-1]
        connectivity = forward_connectivity + backward_connectivity
        J_Z = 0.5**3*np.multiply.outer(connectivity, np.diag([0, 0, 1]))
        J_XX_YY = 0.5**3*np.multiply.outer(connectivity, np.diag([1, 1, 0]))
        # Check the minus sign convention in the below definition. is it XY-YX
        #   or YX-XY

        J_XY_YX = 0.5**3*np.multiply.outer((np.einsum("ij,j...->ij...", np.eye(spins, spins, 0), np.eye(spins, spins, 1))
                                -np.einsum("ij,j...->ij...", np.eye(spins, spins, 1), np.eye(spins, spins, -1)))[:-1],
                                np.array([[0, 1, 0], 
                                          [-1, 0, 0], 
                                          [0, 0, 0]]))
        # one factor of 0.5 is for double counting, the other two are the
        #   factors of two differences between spin operators and Pauli
        #   operators
        J = np.stack([J_Z, J_XX_YY, J_XY_YX])
        if feromagnetic: J *= -1
        self._ferromagnetic = feromagnetic
        QubitSystem.__init__(self,
                             QubitSpace(spins),
                             single_qubit_drift_coefficients,
                             np.zeros((spins, spins, 3, 3)),
                             single_qubit_ctrl_coefficients,
                             J,
                             use_graph)
    @property
    def ferromagnetic(self) -> bool:
        """
        Whether the exchange coupling is ferromagnetic or antiferromagnetic
        """
        return self._ferromagnetic