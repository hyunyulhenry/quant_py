#!/usr/bin/env python
# coding: utf-8

# # 파이썬 다운로드 및 설치하기
# 
# 파이썬 프로그램은 공식 홈페이지(https://www.python.org/)에서 직접 다운로드하여 설치할 수 있다. 그러나 아나콘다(Anaconda)를 설치하면 파이썬 뿐만 아니라 IDE, 각종 패키지를 함께 설치할 수 있으므로 훨씬 편리하다. 
# 
# ## 아나콘다 설치하기
# 
# 아나콘다를 설치하기 위해서는 먼저 구글에서 [아나콘다 다운로드]를 검색하거나, 홈페이지(https://www.anaconda.com/products/distribution)에 접속한다. 그 후 본인의 운영체제에 맞는 파일을 다운로드 한다.
# 
# ```{figure} image/install_python/os.png
# ---
# name: os
# ---
# ```
# 
# [Download] 부분을 클릭한다.
# 
# <hr>
# 
# ```{figure} image/install_python/ins1.png
# ---
# name: ins1
# ---
# ```
# 
# 다운로드한 설치 파일을 실행한 후 [Next]를 클릭한다.
# 
# <hr>
# 
# ```{figure} image/install_python/ins2.png
# ---
# name: ins2
# ---
# ```
# 
# [I Agree]를 클릭한다.
# 
# <hr>
# 
# ```{figure} image/install_python/ins3.png
# ---
# name: ins3
# ---
# ```
# 
# [Just Me]를 선택한 후 [Next]를 클릭한다.
# 
# <hr>
# 
# ```{figure} image/install_python/ins4.png
# ---
# name: ins4
# ---
# ```
# 
# 저장경로를 선택한 후 [Next]를 클릭한다.
# 
# <hr>
# 
# ```{figure} image/install_python/ins5.png
# ---
# name: ins5
# ---
# ```
# 
# 아래의 [Register Anaconda3 as my default Python 3.9]를 체크한 후 [Install]을 클릭한다.
# 
# <hr>
# 
# ```{figure} image/install_python/ins6.png
# ---
# name: ins6
# ---
# ```
# 
# ```{figure} image/install_python/ins7.png
# ---
# name: ins7
# ---
# ```
# 
# 설치가 완료되면 [Next]를 클릭한다.
# 
# <hr>
# 
# ```{figure} image/install_python/ins8.png
# ---
# name: ins8
# ---
# ```
# 
# 두 부분 모두 체크를 해제한 후 [Finish]를 클릭해 설치를 마감한다.
# 
# ## 스파이더 사용하기
# 
# 아나콘다에는 파이썬을 쉽게 사용할 수 있게 하기 위해 여러 IDE가 함께 설치된다. 그 중 본 책에서는 Spyder를 사용하도록 한다.
# 
# ```{figure} image/install_python/spyder1.png
# ---
# name: spyder1
# ---
# ```
# 
# 먼저 검색창에서 [spyder]를 검색하여 'Spyder (anaconda3)' 프로그램을 연다.
# 
# <hr>
# 
# ```{figure} image/install_python/spyder2.png
# ---
# name: spyder2
# ---
# ```
# 
# 스파이더는 크게 3개의 화면으로 구성되어 있다.
# 
# 1. Editor 창: 파이썬 코드를 작성하는 곳으로써, 이곳에서 작성된 스크립트는 F9나 Ctrl+Enter 등을 사용해 명시적으로 실행을 시켜야만 실행이 된다. 보통 이곳에서 코드를 작성한 후 파일로 저장한다.
# 2. Variable Explorer: 현재 입력된 변수 및 값이 무엇인지 확인할 수 있으며, 그 외에도 Plot이나 File 등을 확인할 수 있는 탭도 있다.
# 3. IPython 콘솔: 에디터 창에서 입력한 코드를 실행하면 이 부분에 결과가 출력되며, 파이썬 명령을 직접 입력하여 결과를 확인할 수도 있다.
# 
# <hr>
# 
# ```{figure} image/install_python/spyder3.png
# ---
# name: spyder3
# ---
# ```
# 
# 스크립트 창에 코드를 입력해보자. 그 후 실행하고자 하는 부분을 드래그해 F9 키를 누르면 해당 부분이 콘솔창에 입력되면서 `print('Hello World')`에 해당하는 코드가 실행된다.
# 
# <hr>
# 
# ```{figure} image/install_python/spyder4.png
# ---
# name: spyder4
# ---
# ```
# 
# 콘솔창에서 바로 코드를 입력할 수도 있다. `1+2`를 입력하면 결과값인 `3`이 출력된다.
# 
# <hr>
# 
# ```{figure} image/install_python/spyder5.png
# ---
# name: spyder5
# ---
# ```
# 
# 코드를 통해 변수를 입력해보자. `a = 1`을 입력한 후 우측 상단의 'Variable Explorer'를 확인해보면 a라는 변수에 1이라는 값이 입력된 것을 확인할 수 있다.
