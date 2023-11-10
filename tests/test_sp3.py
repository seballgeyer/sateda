import copy
import unittest

from io import StringIO
import numpy as np

from sateda.io.sp3.sp3 import sp3

input_data = """#dV2007  4 12  0  0  0.00000000     289 ORBIT IGS14 BHN ESOC        
## 1422 345600.00000000   900.00000000 54202 0.0000000000000        
+    2   G01G02  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
+          0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
+          0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
+          0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
+          0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
++         8  8  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0      
++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0      
++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0      
++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0      
++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0      
%c M  cc GPS ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc      
%c cc cc ccc ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc      
%f  0.0000000  0.000000000  0.00000000000  0.000000000000000      
%f  0.0000000  0.000000000  0.00000000000  0.000000000000000      
%i    0    0    0    0      0      0      0      0         0      
%i    0    0    0    0      0      0      0      0         0      
/*   EUROPEAN SPACE OPERATIONS CENTRE - DARMSTADT, GERMANY        
/* ---------------------------------------------------------      
/*  SP3 FILE GENERATED BY NAPEOS BAHN TOOL  (DETERMINATION)         
/* PCV:IGS14_2022 OL/AL:EOT11A   NONE     YN ORB:CoN CLK:CoN        
*  2007  4 12  0  0  0.00000000                                      
PG01  -6114.801556 -13827.040252  22049.171610 999999.999999           
VG01  27184.457428  -3548.055474   5304.058806 999999.999999          
PG02  12947.223282  22448.220655   6215.570741 999999.999999         
VG02  -7473.756152  -4355.288568  29939.333728 999999.999999      
*  2007  4 12  0 15  0.00000000                                      
PG01  -3659.032812 -14219.662913  22339.175481 999999.999999          
VG01  27295.435569  -5170.061971   1131.227754 999999.999999          
PG02  12163.580358  21962.803659   8849.429007 999999.999999          
VG02  -9967.334764  -6367.969150  28506.683280 999999.999999          
*  2007  4 12  0 30  0.00000000                                       
PG01  -1218.171155 -14755.013599  22252.168480 999999.999999          
VG01  26855.435366  -6704.236117  -3062.394499 999999.999999          
PG02  11149.555664  21314.099837  11331.977499 999999.999999           
VG02 -12578.915944  -7977.396362  26581.116225 999999.999999 """


input_data2 = """#dV2007  4 11  0  0  0.00000000     289 ORBIT IGS14 BHN ESOC
## 1422 345600.00000000   900.00000000 54202 0.0000000000000         
+    2   G01G02  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
+          0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
+          0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
+          0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
+          0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0          
++         8  8  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0           
%c M  cc GPS ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc           
%c cc cc ccc ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc           
%f  0.0000000  0.000000000  0.00000000000  0.000000000000000          
%f  0.0000000  0.000000000  0.00000000000  0.000000000000000           
%i    0    0    0    0      0      0      0      0         0           
%i    0    0    0    0      0      0      0      0         0           
/*   EUROPEAN SPACE OPERATIONS CENTRE - DARMSTADT, GERMANY             
/* ---------------------------------------------------------           
/*  SP3 FILE GENERATED BY NAPEOS BAHN TOOL  (DETERMINATION)            
/* PCV:IGS14_2022 OL/AL:EOT11A   NONE     YN ORB:CoN CLK:CoN           
*  2007  4 11  0  0  0.00000000                                        
PG01   76114.80155 -14827.040252   2049.171610 999999.999999          
VG01  27184.457428  -3548.055474   5304.058806 999999.999999          
PG02  10947.223282  20448.220655  16215.570741 999999.999999          
VG02  -7473.756152  -4355.288568  29939.333728 999999.999999      
*  2007  4 11  0 15  0.00000000                                       
PG01  -3659.032812 -14219.662913  22339.175481 999999.999999          
VG01  27295.435569  -5170.061971   1131.227754 999999.999999          
PG02  12163.580358  21962.803659   8849.429007 999999.999999          
VG02  -9967.334764  -6367.969150  28506.683280 999999.999999          
*  2007  4 11  0 30  0.00000000                                       
PG01  -1218.171155 -14755.013599  22252.168480 999999.999999          
VG01  26855.435366  -6704.236117  -3062.394499 999999.999999          
PG02  11149.555664  21314.099837  11331.977499 999999.999999          
VG02 -12578.915944  -7977.396362  26581.116225 999999.999999"""


class TestSp3(unittest.TestCase):
    def setUp(self) -> None:
        print("In method", self._testMethodName)
        self.sp3_data = sp3()
        self.sp3_data = sp3.read(file_or_string=StringIO(input_data))

        self.sp3_data2 = sp3().read(file_or_string=StringIO(input_data2))

    def test_headerNsat(self):
        print(self.sp3_data.header)
        self.assertEqual(self.sp3_data.header["nsat"], 2)  # add assertion here

    def test_merge1(self):
        """
        Testing the merge functions.
        """
        print("reading data")
        s1 = sp3().read(file_or_string=StringIO(input_data))
        s2 = sp3().read(file_or_string=StringIO(input_data2))
        s1.merge(self.sp3_data2)
        s2.merge(self.sp3_data)
        # check if the x values are the same
        self.assertTrue(np.all(s1.data["G01"]["time"] == s2.data["G01"]["time"]))
        self.assertTrue(np.all(s1.data["G02"]["time"] == s2.data["G02"]["time"]))
        self.assertTrue(np.all(s1.data["G01"]["x"] == s2.data["G01"]["x"]))
        self.assertTrue(np.all(s1.data["G02"]["x"] == s2.data["G02"]["x"]))
        self.assertTrue(np.all(s1.data["G01"]["y"] == s2.data["G01"]["y"]))
        self.assertTrue(np.all(s1.data["G02"]["y"] == s2.data["G02"]["y"]))
        self.assertTrue(np.all(s1.data["G01"]["z"] == s2.data["G01"]["z"]))
        self.assertTrue(np.all(s1.data["G02"]["z"] == s2.data["G02"]["z"]))


if __name__ == "__main__":
    unittest.main()
