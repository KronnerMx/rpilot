from selfdrive.car import dbc_dict

class CAR:
  GOLF = "2018 VW Golf R"
  ATLAS = "2018 VW Atlas SEL Premium"
  OCTAVIA = "Skoda Octavia"

FINGERPRINTS = {
  CAR.GOLF: [
    {64: 8, 134: 8, 159: 8, 173: 8, 178: 8, 253: 8, 257: 8, 260: 8, 262: 8, 264: 8, 278: 8, 279: 8, 283: 8, 286: 8,
     288: 8, 289: 8, 290: 8, 294: 8, 299: 8, 302: 8, 346: 8, 418: 8, 427: 8, 679: 8, 681: 8, 695: 8, 779: 8, 780: 8,
     783: 8, 792: 8, 795: 8, 804: 8, 806: 8, 807: 8, 808: 8, 809: 8, 870: 8, 896: 8, 897: 8, 898: 8, 901: 8, 917: 8,
     919: 8, 949: 8, 958: 8, 960: 4, 981: 8, 987: 8, 988: 8, 991: 8, 997: 8, 1000: 8, 1019: 8, 1122: 8, 1123: 8,
     1124: 8, 1153: 8, 1162: 8, 1175: 8, 1312: 8, 1385: 8, 1413: 8, 1440: 5, 1514: 8, 1515: 8, 1520: 8, 1600: 8,
     1601: 8, 1603: 8, 1605: 8, 1624: 8, 1626: 8, 1629: 8, 1631: 8, 1646: 8, 1648: 8, 1712: 6, 1714: 8, 1716: 8,
     1717: 8, 1719: 8, 1720: 8, 1721: 8, 1792: 8
     },
  ],
  CAR.ATLAS: [
    {64: 8, 134: 8, 159: 8, 173: 8, 178: 8, 253: 8, 257: 8, 260: 8, 262: 8, 278: 8, 279: 8, 283: 8, 286: 8, 288: 8,
     289: 8, 290: 8, 294: 8, 299: 8, 302: 8, 346: 8, 418: 8, 427: 8, 679: 8, 681: 8, 695: 8, 779: 8, 780: 8, 783: 8,
     792: 8, 804: 8, 806: 8, 807: 8, 808: 8, 809: 8, 870: 8, 896: 8, 897: 8, 898: 8, 901: 8, 917: 8, 919: 8, 927: 8,
     949: 8, 958: 8, 960: 4, 981: 8, 987: 8, 988: 8, 991: 8, 997: 8, 1000: 8, 1019: 8, 1122: 8, 1123: 8, 1124: 8,
     1153: 8, 1162: 8, 1175: 8, 1312: 8, 1351: 8, 1385: 8, 1413: 8, 1440: 5, 1514: 8, 1515: 8, 1520: 8, 1600: 8,
     1601: 8, 1603: 8, 1605: 8, 1624: 8, 1629: 8, 1631: 8, 1646: 8, 1648: 8, 1712: 6, 1714: 8, 1716:8, 1717: 8,
     1719: 8, 1720: 8, 1721: 8, 1792: 8
     },
    {64: 8, 134: 8, 159: 8, 173: 8, 178: 8, 253: 8, 257: 8, 260: 8, 262: 8, 278: 8, 283: 8, 286: 8, 288: 8, 289: 8, 
     299: 8, 346: 8, 418: 8, 427: 8, 779: 8, 795: 8, 870: 8, 896: 8, 897: 8, 898: 8, 901: 8, 927: 8, 949: 8, 958: 8, 
     960: 4, 981: 8, 987: 8, 988: 8, 991: 8, 997: 8, 1000: 8, 1019: 8, 1122: 8, 1123: 8, 1124: 8, 1153: 8, 1156: 8, 
     1157: 8, 1158: 8, 1175: 8, 1312: 8, 1385: 8, 1413: 8, 1440: 5, 1471: 4, 1514: 8, 1515: 8, 1520: 8, 1600: 8, 
     1601: 8, 1603: 8, 1624: 8, 1626: 8, 1629: 8, 1631: 8, 1635: 8, 1646: 8, 1648: 8, 1712: 6, 1714: 8, 1716: 8, 
     1717: 8, 1719: 8, 1720: 8
     },
  ],
  CAR.OCTAVIA: [
    {64: 8, 134: 8, 159: 8, 173: 8, 178: 8, 253: 8, 257: 8, 262: 8, 278: 8, 279: 8, 285: 8, 286: 8, 288: 8, 289: 8,
     290: 8, 299: 8, 302: 8, 427: 8, 779: 8, 780: 8, 804: 8, 870: 8, 901: 8, 917: 8, 929: 8, 930: 8, 949: 8, 958: 8,
     960: 4, 981: 8, 987: 8, 988: 8, 991: 8, 997: 8, 1153: 8, 1175: 8, 1312: 8, 1385: 8, 1413: 8, 1440: 5, 1514: 8,
     1515: 8, 1520: 8, 1600: 8, 1601: 8, 1603: 8, 1624: 8, 1629: 8, 1631: 8, 1646: 8, 1648: 8, 1712: 6, 1714: 8,
     1716: 8, 1717: 8, 1719: 8, 1720: 8
     },
  ],
}

DBC = {
  CAR.GOLF: dbc_dict('vw_mqb_2010', None),
  CAR.ATLAS: dbc_dict('vw_mqb_2010', None),
  CAR.OCTAVIA: dbc_dict('vw_mqb_2010', None),
}
