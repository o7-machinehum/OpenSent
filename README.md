#OpenSent
Open source project for mining twitter sentiment data on cryptocurrencies and finding an auto
correlation between price and sentiment. Credit to stocktalk for code in 'stocktalk' folder.<br\>
<br\>

[Paper V0.1 here](https://github.com/Machine-Hum/cryptos/blob/master/paper/paper.pdf)
<br\><br\>

![Plot](/Datasets/Plots/Dec4-8.eps)

├── coinmarketcap_cache.sqlite
├── Datasets
│   ├── BatchLagFinder.m
│   ├── batchOutput
│   │   ├── OctListing
│   │   ├── plots
│   │   │   ├── DerivShifted
│   │   │   │   └── Oct
│   │   │   │       ├── Oct10.csv.png
│   │   │   │       ├── Oct11.csv.png
│   │   │   │       ├── Oct12.csv.png
│   │   │   │       ├── Oct13.csv.png
│   │   │   │       ├── Oct15.csv.png
│   │   │   │       ├── Oct16.csv.png
│   │   │   │       ├── Oct17.csv.png
│   │   │   │       ├── Oct18.csv.png
│   │   │   │       ├── Oct2.csv.png
│   │   │   │       ├── Oct3.csv.png
│   │   │   │       ├── Oct4.csv.png
│   │   │   │       ├── Oct5.csv.png
│   │   │   │       ├── Oct6.csv.png
│   │   │   │       ├── Oct7.csv.png
│   │   │   │       ├── Oct8.csv.png
│   │   │   │       ├── Oct9.csv.png
│   │   │   │       └── Sept29-Oct1.csv.png
│   │   │   ├── DerivShifted_CorrVector
│   │   │   │   └── Oct
│   │   │   │       ├── Oct10.csv.png
│   │   │   │       ├── Oct11.csv.png
│   │   │   │       ├── Oct12.csv.png
│   │   │   │       ├── Oct13.csv.png
│   │   │   │       ├── Oct15.csv.png
│   │   │   │       ├── Oct16.csv.png
│   │   │   │       ├── Oct17.csv.png
│   │   │   │       ├── Oct18.csv.png
│   │   │   │       ├── Oct2.csv.png
│   │   │   │       ├── Oct3.csv.png
│   │   │   │       ├── Oct4.csv.png
│   │   │   │       ├── Oct5.csv.png
│   │   │   │       ├── Oct6.csv.png
│   │   │   │       ├── Oct7.csv.png
│   │   │   │       ├── Oct8.csv.png
│   │   │   │       ├── Oct9.csv.png
│   │   │   │       └── Sept29-Oct1.csv.png
│   │   │   ├── MagShifted
│   │   │   │   └── Oct
│   │   │   │       ├── Oct10.csv.png
│   │   │   │       ├── Oct11.csv.png
│   │   │   │       ├── Oct12.csv.png
│   │   │   │       ├── Oct13.csv.png
│   │   │   │       ├── Oct15.csv.png
│   │   │   │       ├── Oct16.csv.png
│   │   │   │       ├── Oct17.csv.png
│   │   │   │       ├── Oct18.csv.png
│   │   │   │       ├── Oct2.csv.png
│   │   │   │       ├── Oct3.csv.png
│   │   │   │       ├── Oct4.csv.png
│   │   │   │       ├── Oct5.csv.png
│   │   │   │       ├── Oct6.csv.png
│   │   │   │       ├── Oct7.csv.png
│   │   │   │       ├── Oct8.csv.png
│   │   │   │       ├── Oct9.csv.png
│   │   │   │       └── Sept29-Oct1.csv.png
│   │   │   └── MagShifted_CorrVector
│   │   │       └── Oct
│   │   │           ├── Oct10.csv.png
│   │   │           ├── Oct11.csv.png
│   │   │           ├── Oct12.csv.png
│   │   │           ├── Oct13.csv.png
│   │   │           ├── Oct15.csv.png
│   │   │           ├── Oct16.csv.png
│   │   │           ├── Oct17.csv.png
│   │   │           ├── Oct18.csv.png
│   │   │           ├── Oct2.csv.png
│   │   │           ├── Oct3.csv.png
│   │   │           ├── Oct4.csv.png
│   │   │           ├── Oct5.csv.png
│   │   │           ├── Oct6.csv.png
│   │   │           ├── Oct7.csv.png
│   │   │           ├── Oct8.csv.png
│   │   │           ├── Oct9.csv.png
│   │   │           └── Sept29-Oct1.csv.png
│   │   └── SeptListing
│   ├── batch.sh
│   ├── Contig
│   │   ├── Oct15.csv
│   │   ├── Oct16.csv
│   │   ├── Oct17.csv
│   │   ├── Oct18.csv
│   │   ├── Oct19.csv
│   │   ├── Oct21.csv
│   │   ├── Oct22.csv
│   │   ├── Oct23.csv
│   │   ├── Oct24.csv
│   │   ├── Oct25.csv
│   │   ├── Oct26.csv
│   │   ├── Oct27.csv
│   │   ├── Oct28.csv
│   │   ├── Oct29.csv
│   │   ├── Oct30.csv
│   │   └── Oct31.csv
│   ├── Dec
│   │   ├── Dec01.csv
│   │   ├── Dec04.csv
│   │   ├── Dec05.csv
│   │   ├── Dec06.csv
│   │   ├── Dec07.csv
│   │   ├── Dec08.csv
│   │   ├── Dec09.csv
│   │   ├── Dec10.csv
│   │   ├── Dec12.csv
│   │   ├── Dec13.csv
│   │   ├── Dec14.csv
│   │   ├── Dec15.csv
│   │   ├── Dec16.csv
│   │   ├── Dec17.csv
│   │   ├── Dec18.csv
│   │   ├── Dec19.csv
│   │   ├── Dec20.csv
│   │   ├── Dec21.csv
│   │   ├── Dec22.csv
│   │   ├── Dec23.csv
│   │   ├── Dec24.csv
│   │   ├── Dec25.csv
│   │   └── Dec26.csv
│   ├── FFT.m
│   ├── fname
│   ├── Fourier.m
│   ├── FractalLagFinder.m
│   ├── LagFinder.m
│   ├── Nov
│   │   ├── Nov01.csv
│   │   ├── Nov02.csv
│   │   ├── Nov03.csv
│   │   ├── Nov04.csv
│   │   ├── Nov05.csv
│   │   ├── Nov06.csv
│   │   ├── Nov07.csv
│   │   ├── Nov08.csv
│   │   ├── Nov09.csv
│   │   ├── Nov10.csv
│   │   ├── Nov11.csv
│   │   ├── Nov12.csv
│   │   ├── Nov13.csv
│   │   ├── Nov14.csv
│   │   ├── Nov15.csv
│   │   ├── Nov16.csv
│   │   └── Nov17.csv
│   ├── Oct
│   │   ├── Oct10.csv
│   │   ├── Oct11.csv
│   │   ├── Oct12.csv
│   │   ├── Oct13.csv
│   │   ├── Oct15.csv
│   │   ├── Oct16.csv
│   │   ├── Oct17.csv
│   │   ├── Oct18.csv
│   │   ├── Oct19.csv
│   │   ├── Oct21.csv
│   │   ├── Oct22.csv
│   │   ├── Oct23.csv
│   │   ├── Oct24.csv
│   │   ├── Oct25.csv
│   │   ├── Oct26.csv
│   │   ├── Oct27.csv
│   │   ├── Oct28.csv
│   │   ├── Oct29.csv
│   │   ├── Oct2.csv
│   │   ├── Oct30.csv
│   │   ├── Oct31.csv
│   │   ├── Oct3.csv
│   │   ├── Oct4.csv
│   │   ├── Oct5.csv
│   │   ├── Oct6.csv
│   │   ├── Oct7.csv
│   │   ├── Oct8.csv
│   │   ├── Oct9.csv
│   │   └── Sept29-Oct1.csv
│   ├── octave-workspace
│   ├── Plots
│   │   ├── Dec21-23.eps
│   │   ├── Dec21-23.pdf
│   │   ├── Dec23.eps
│   │   ├── Dec23.pdf
│   │   ├── Dec26.eps
│   │   ├── Dec26.pdf
│   │   ├── Dec4-8.eps
│   │   ├── Dec4-8.pdf
│   │   ├── First_Plots
│   │   │   ├── 1-First.png
│   │   │   ├── 2-LPF.png
│   │   │   ├── 3-Shifted_6hr.png
│   │   │   └── 4-dsdt.png
│   │   ├── Fractal_Analasys
│   │   │   ├── Oct2-6FracSep.png
│   │   │   ├── Oct2-6.png
│   │   │   └── Oct2-6VectorAvg.png
│   │   ├── meanTimeshifts
│   │   │   ├── Oct2.png
│   │   │   ├── Oct3.png
│   │   │   └── Oct4.png
│   │   ├── Oct7_CostSen.eps
│   │   ├── Oct7_CostSen.pdf
│   │   ├── Oct7_K.eps
│   │   ├── Oct7_K.pdf
│   │   ├── Oct9_Sen.eps
│   │   ├── Oct9_Sen_Fil.eps
│   │   ├── Oct9_Sen_Fil.pdf
│   │   ├── Oct9_Sen.pdf
│   │   ├── senShifts
│   │   │   ├── Oct2.png
│   │   │   ├── Oct3.png
│   │   │   └── Oct4.png
│   │   ├── Sept19-21
│   │   │   ├── Screenshot from 2017-09-21 23-38-18.png
│   │   │   └── Screenshot from 2017-09-21 23-38-40.png
│   │   ├── Sept19-25
│   │   │   └── P1.png
│   │   ├── Sept29-Oct1
│   │   │   ├── Screenshot from 2017-10-01 12-24-47.png
│   │   │   └── Screenshot from 2017-10-01 12-25-26.png
│   │   ├── TweetVolume.eps
│   │   ├── TweetVolume.pdf
│   │   ├── VectorSumk.eps
│   │   └── VectorSumk.pdf
│   ├── post.m
│   ├── post.py
│   ├── Sept
│   │   ├── Sept17_2017.csv
│   │   ├── Sept19-21.csv
│   │   ├── Sept19-26.csv
│   │   ├── Sept20_2017.csv
│   │   └── Sept21_2017.csv
│   └── test
│       └── trendTest.csv
├── fetch.py
├── log
│   ├── 2017-12-15
│   ├── 2017-12-17
│   ├── 2017-12-18
│   ├── 2017-12-19
│   ├── 2017-12-20
│   ├── 2017-12-21
│   ├── 2017-12-22
│   ├── 2017-12-23
│   ├── 2017-12-24
│   ├── 2017-12-25
│   └── 2017-12-26
├── mainboot.sh
├── paper
│   ├── changelog.txt
│   ├── IEEEtran.cls
│   ├── Makefile
│   ├── paper.aux
│   ├── paper.log
│   ├── paper.pdf
│   ├── paper.tex
│   └── README.txt
├── __pycache__
│   ├── fetch.cpython-35.pyc
│   └── fetchPrice.cpython-35.pyc
├── README.md
├── restart.txt
├── RT
│   ├── Log.py
│   ├── Notifier.py
│   ├── push.py
│   ├── __pycache__
│   │   ├── Log.cpython-35.pyc
│   │   ├── Logging.cpython-35.pyc
│   │   ├── push.cpython-35.pyc
│   │   └── RT.cpython-35.pyc
│   ├── README
│   └── RT.py
├── run.py
├── run.sh
├── setup.py
├── Simulator
│   ├── Makefile
│   ├── Market.py
│   ├── out
│   ├── __pycache__
│   │   ├── Market.cpython-34.pyc
│   │   ├── Market.cpython-35.pyc
│   │   └── Market.cpython-36.pyc
│   ├── README.txt
│   ├── tags
│   ├── Test.py
│   └── wlkr.py
├── stocktalk
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── fetch.cpython-35.pyc
│   │   ├── __init__.cpython-35.pyc
│   │   ├── streaming.cpython-35.pyc
│   │   └── visualize.cpython-35.pyc
│   ├── streaming.py
│   └── visualize.py
└── vis.py
