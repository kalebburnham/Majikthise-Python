import sys
sys.path.append('../majikthise')

import unittest

from bitboard import *
from board import *

class BitboardTests(unittest.TestCase):

	

	def test_bsf_0b00(self):
		self.assertRaises(AssertionError, BSF, np.uint64(0b00))

	def test_bsf_0b1000(self):
		b = np.uint64(0b1000)
		self.assertEqual(BSF(b), 3)

	def test_bsf_0b1110(self):
		b = np.uint64(0b1110)
		self.assertEqual(BSF(b), 1)

	def test_bsf_0xFFFFFF00(self):
		b = np.uint64(0xFFFFFF00)
		self.assertEqual(BSF(b), 8)

	def test_bsf_0x8000000000000000(self):
		b = np.uint64(0x8000000000000000)
		self.assertEqual(BSF(b), np.uint64(63))

	def test_bsf_17179869219(self):
		b = np.uint64(17179869219)
		self.assertEqual(BSF(b), 4)

	def test_bsr_0b00(self):
		self.assertRaises(AssertionError, BSR, np.uint64(0b00))

	def test_bsr_0b01(self):
		self.assertEqual(BSR(np.uint64(0b01)), 0)

	def test_bsr_0b11(self):
		self.assertEqual(BSR(np.uint64(0b11)), 1)

	def test_bsr_0x8000000000000000(self):
		b = np.uint64(0b1000000000000000000000000000000000000000000000000000000000000000)
		self.assertEqual(BSR(b), 63)


	def test_generateBoard(self):
		b = CBoard()
		self.assertEqual(b.whitePawns, SECOND_RANK)

if __name__ == '__main__':
	unittest.main()