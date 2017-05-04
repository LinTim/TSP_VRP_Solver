# TSP & VRP 問題應用 TABU Search 的方法求解

 - 求解方式為倆倆替換，如果發現路徑變小，那麼就保留替換後的結果，持續這樣做直到沒有可以替換的為止。
 - 使用Python2去實作

### TSP
 - 旅行銷售員問題（TSP）是給定一系列城市和每對城市之間的距離，求解訪問每一座城市一次並回到起始城市的最短迴路。
 - The structure of the files is as follows:
    1. number of customers
    2. names and coordinates of the customers

### VRP
 - 車輛途程問題（VRP）它是指一定數量的客戶，各自有不同數量的貨物需求，配送中心向客戶提供貨物，由一個車隊負責分送貨物，組織適當的行車路線，目標是使得客戶的需求得到滿足，並能在一定的約束下，達到諸如路程最短、成本最小、耗費時間最少等目的。
 - The structure of the files is as follows:
   1. number of nodes
   2. coordinates for each node
   3. vehicle capacity
   4. demand for each node (Demand of the depot is 0)

# 使用注意
 - 要求解的檔案需要放在與程式同一目錄下
 - filename要完整的輸入(包含附檔名)
 - 求解出來的檔案會存成 1_TS_原檔名.txt