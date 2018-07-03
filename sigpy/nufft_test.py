import unittest
import pickle
import numpy as np
import numpy.testing as npt
from sigpy import nufft, util

if __name__ == '__main__':
    unittest.main()


class TestNufft(unittest.TestCase):

    def test_nufft(self):

        # Check deltas
        ishape = [3]
        input = np.array([0, 1, 0], np.complex)  # delta
        coord = np.array([[-1], [0], [1]], np.float)

        npt.assert_allclose(nufft.nufft(input, coord),
                            np.array([1.0, 1.0, 1.0]) / (3**0.5),
                            atol=0.01, rtol=0.01)

        ishape = [4]
        input = np.array([0, 0, 1, 0], np.complex)  # delta
        coord = np.array([[-2], [-1], [0], [1]], np.float)

        npt.assert_allclose(nufft.nufft(input, coord),
                            np.array([1.0, 1.0, 1.0, 1.0]) / (4**0.5),
                            atol=0.01, rtol=0.01)

        ishape = [5]
        input = np.array([0, 0, 1, 0, 0], np.complex)  # delta
        coord = np.array([[-2], [-1], [0], [1], [2]], np.float)

        npt.assert_allclose(nufft.nufft(input, coord),
                            np.ones(5) / (5**0.5),
                            atol=0.01, rtol=0.01)

        # Check shifted delta
        ishape = [3]
        input = np.array([0, 0, 1], np.complex)  # shifted delta
        coord = np.array([[-1], [0], [1]], np.float)

        w = np.exp(-1j * 2.0 * np.pi / 3.0)
        npt.assert_allclose(nufft.nufft(input, coord),
                            np.array([w.conjugate(), 1.0, w]) / (3**0.5),
                            atol=0.01, rtol=0.01)

        ishape = [4]
        input = np.array([0, 0, 0, 1], np.complex)  # delta
        coord = np.array([[-2], [-1], [0], [1]], np.float)

        w = np.exp(-1j * 2.0 * np.pi / 4.0)
        npt.assert_allclose(nufft.nufft(input, coord),
                            np.array([w.conjugate()**2, w.conjugate(), 1.0, w]) / (4**0.5),
                            atol=0.01, rtol=0.01)


    def test_nufft_nd(self):

        for ndim in range(3):
            ishape = [3, 1]
            
            input = np.array([[0], [1], [0]], np.complex)
            coord = np.array([[-1, 0],
                              [0, 0],
                              [1, 0]], np.float)

            npt.assert_allclose(nufft.nufft(input, coord),
                                np.array([1.0, 1.0, 1.0]) / 3**0.5,
                                atol=0.01, rtol=0.01)


    def test_nufft_adjoint(self):

        # Check deltas
        oshape = [3]
        input = np.array([1.0, 1.0, 1.0], dtype=np.complex) / 3**0.5
        coord = np.array([[-1], [0], [1]], np.float)

        npt.assert_allclose(nufft.nufft_adjoint(input, coord, oshape),
                            np.array([0, 1, 0]),
                            atol=0.01, rtol=0.01)

        oshape = [4]
        input = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.complex) / 4**0.5
        coord = np.array([[-2], [-1], [0], [1]], np.float)

        npt.assert_allclose(nufft.nufft_adjoint(input, coord, oshape),
                            np.array([0, 0, 1, 0], np.complex),
                            atol=0.01, rtol=0.01)

        oshape = [5]
        input = np.ones(5, dtype=np.complex) / 5**0.5
        coord = np.array([[-2], [-1], [0], [1], [2]], np.float)

        npt.assert_allclose(nufft.nufft_adjoint(input, coord, oshape),
                            np.array([0, 0, 1, 0, 0], np.complex),
                            atol=0.01, rtol=0.01)

        # Check shifted delta
        oshape = [3]
        w = np.exp(-1j * 2.0 * np.pi / 3.0)
        input = np.array([w.conjugate(), 1.0, w]) / 3**0.5
        coord = np.array([[-1], [0], [1]], np.float)

        npt.assert_allclose(nufft.nufft_adjoint(input, coord, oshape),
                            np.array([0, 0, 1], np.complex),
                            atol=0.01, rtol=0.01)

        oshape = [4]
        w = np.exp(-1j * 2.0 * np.pi / 4.0)
        input = np.array([w.conjugate()**2, w.conjugate(), 1.0, w]) / 4**0.5
        coord = np.array([[-2], [-1], [0], [1]], np.float)

        npt.assert_allclose(nufft.nufft_adjoint(input, coord, oshape),
                            np.array([0, 0, 0, 1], np.complex),
                            atol=0.01, rtol=0.01)

    def test_nufft_adjoint_nd(self):

        oshape = [3, 1]

        input = np.array([1.0, 1.0, 1.0], dtype=np.complex) / 3**0.5
        coord = np.array([[-1, 0],
                          [0, 0],
                          [1, 0]], np.float)

        npt.assert_allclose(nufft.nufft_adjoint(input, coord, oshape),
                            np.array([[0], [1], [0]], np.complex),
                            atol=0.01, rtol=0.01)

    def test_nufft_normal(self):
        
        # Check delta
        oshape = [3]
        input = np.array([0.0, 1.0, 0.0], dtype=np.complex)
        coord = np.array([[-1], [0], [1]], np.float)

        npt.assert_allclose(nufft.nufft_adjoint(nufft.nufft(input, coord), coord, oshape),
                            np.array([0, 1, 0]),
                            atol=0.01, rtol=0.01)

        # Check delta scale
        oshape = [3]
        input = np.array([0.0, 1.0, 0.0], dtype=np.complex)
        coord = np.array([[-1], [-0.5], [0], [0.5], [1]], np.float)

        npt.assert_allclose(nufft.nufft_adjoint(nufft.nufft(input, coord),
                                                coord, oshape)[len(input) // 2],
                            5 / 3,
                            atol=0.01, rtol=0.01)

    def test_nufft_ndft(self):

        n = 5
        w = np.exp(-1j * 2 * np.pi / n)
        coord = np.array([[-2], [0], [0.1]])
        w2 = w**-2
        w1 = w**0.1
        A = np.array([[w2**-2, w2**-1, 1, w2, w2**2],
                      [1, 1, 1, 1, 1],
                      [w1**-2, w1**-1, 1, w1, w1**2]]) / n**0.5

        for i in range(n):
            input = np.zeros(n, np.complex)
            input[i] = 1
            npt.assert_allclose(A[:, i], nufft.nufft(input, coord), atol=0.01, rtol=0.01)

        n = 6
        w = np.exp(-1j * 2 * np.pi / n)
        coord = np.array([[-2], [0], [0.1]])
        w2 = w**-2
        w1 = w**0.1
        A = np.array([[w2**-3, w2**-2, w2**-1, 1, w2, w2**2],
                      [1, 1, 1, 1, 1, 1],
                      [w1**-3, w1**-2, w1**-1, 1, w1, w1**2]]) / n**0.5
        
        for i in range(n):
            input = np.zeros(n, np.complex)
            input[i] = 1
            npt.assert_allclose(A[:, i], nufft.nufft(input, coord), atol=0.01, rtol=0.01)
             
